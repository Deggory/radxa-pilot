#include <CL/cl.h>
#include <cassert>
#include <cstring>
#include <map>
#include <memory>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include "selfdrive/modeld/thneed/thneed.h"

// Use comma's original PC execute/clexec and kernel replay, on an existing
// GPU context. This bridge adapts current Tinygrad's capture, not its kernels.
cl_device_id cl_get_device_id(cl_device_type) {
  cl_uint count=0;
  if (clGetPlatformIDs(0,nullptr,&count)!=CL_SUCCESS) return nullptr;
  std::vector<cl_platform_id> platforms(count);
  clGetPlatformIDs(count,platforms.data(),nullptr);
  for (auto platform:platforms) {
    cl_device_id gpu=nullptr;
    if (clGetDeviceIDs(platform,CL_DEVICE_TYPE_GPU,1,&gpu,nullptr)==CL_SUCCESS) return gpu;
  }
  return nullptr;
}

namespace {
thread_local std::string error;
struct Replay {
  Thneed model;
  std::vector<cl_mem> memory;
  std::vector<cl_program> programs;
  explicit Replay(cl_context context,cl_device_id device,cl_command_queue queue,cl_mem output):model(false,context) {
    model.device_id=device; model.command_queue=queue; model.output=output;
    if (clRetainContext(context)!=CL_SUCCESS || clRetainCommandQueue(queue)!=CL_SUCCESS)
      throw std::runtime_error("retain context/queue failed");
  }
  ~Replay() {
    for (auto &k:model.kq) if(k->kernel) clReleaseKernel(k->kernel);
    for (auto p:programs) clReleaseProgram(p);
    for (auto m:memory) clReleaseMemObject(m);
    clReleaseCommandQueue(model.command_queue); clReleaseContext(model.context);
  }
};
void check(cl_int value) { if(value!=CL_SUCCESS) throw std::runtime_error("OpenCL "+std::to_string(value)); }
}

const char *cl_get_error_string(int) { return "OpenCL error (see return code)"; }
cl_program cl_program_from_source(cl_context context,cl_device_id device,const std::string &source) {
  const char *data=source.data(); size_t size=source.size(); cl_int error;
  auto program=clCreateProgramWithSource(context,1,&data,&size,&error); check(error);
  check(clBuildProgram(program,1,&device,nullptr,nullptr,nullptr)); return program;
}
cl_program cl_program_from_binary(cl_context context,cl_device_id device,const uint8_t *binary,size_t size) {
  cl_int status,error;
  auto program=clCreateProgramWithBinary(context,1,&device,&size,&binary,&status,&error); check(error); check(status);
  check(clBuildProgram(program,1,&device,nullptr,nullptr,nullptr)); return program;
}

extern "C" {
const char *q8b_thneed_error() { return error.c_str(); }
void *q8b_thneed_create(cl_context context,cl_device_id device,cl_command_queue queue,cl_mem output) {
  try {
    cl_device_type type=0; check(clGetDeviceInfo(device,CL_DEVICE_TYPE,sizeof(type),&type,nullptr));
    if(!(type&CL_DEVICE_TYPE_GPU)) throw std::runtime_error("GPU required");
    return new Replay(context,device,queue,output);
  } catch(const std::exception &e) { error=e.what(); return nullptr; }
}
int q8b_thneed_add(void *handle,cl_kernel original,unsigned dims,const size_t *global,const size_t *local,
                   unsigned count,const size_t *sizes,const void *const *values) {
  try {
    if(!handle || !original || !global || !local || dims==0 || dims>3 || count>256 || !sizes || !values)
      throw std::runtime_error("invalid replay metadata");
    auto &r=*static_cast<Replay*>(handle);
    auto k=std::make_shared<CLQueuedKernel>(&r.model);
    char name[1024]{}; cl_program program=nullptr;
    check(clGetKernelInfo(original,CL_KERNEL_FUNCTION_NAME,sizeof(name),name,nullptr));
    check(clGetKernelInfo(original,CL_KERNEL_PROGRAM,sizeof(program),&program,nullptr));
    cl_uint actual=0; check(clGetKernelInfo(original,CL_KERNEL_NUM_ARGS,sizeof(actual),&actual,nullptr));
    if(count!=actual) throw std::runtime_error("kernel argument count mismatch");
    check(clRetainProgram(program)); r.programs.push_back(program);
    k->name=name; k->program=program; k->num_args=count; k->work_dim=dims;
    for(unsigned d=0;d<dims;++d) {
      if(!global[d] || !local[d] || global[d]%local[d]) throw std::runtime_error("invalid global/local dimensions");
      k->global_work_size[d]=global[d]; k->local_work_size[d]=local[d];
    }
    for(unsigned i=0;i<count;++i) {
      if(!sizes[i] || sizes[i]>(1U<<20)) throw std::runtime_error("invalid argument size");
      k->args_size.push_back(int(sizes[i]));
      k->args.emplace_back(values[i]?std::string(static_cast<const char*>(values[i]),sizes[i]):std::string());
      // Current captured graph has cl_mem (8-byte) and 32-bit scalar args.
      // Reject a 64-bit scalar rather than guessing that it is a memory handle.
      if(values[i] && sizes[i]==sizeof(cl_mem)) {
        cl_mem m=nullptr; std::memcpy(&m,values[i],sizeof(m));
        check(clRetainMemObject(m)); r.memory.push_back(m);
      }
    }
    r.model.kq.push_back(k); return 0;
  } catch(const std::exception &e) { error=e.what(); return -1; }
}
int q8b_thneed_run(void *handle,void *output) {
  try {
    if(!handle || !output) throw std::runtime_error("invalid replay/output");
    auto &r=*static_cast<Replay*>(handle);
    if(r.model.kq.empty()) throw std::runtime_error("empty graph");
    // Inputs remain resident. Original PC execute calls clexec + synchronized
    // output copy. No camera, parsing or host input upload is timed here.
    std::vector<float*> inputs(r.model.input_sizes.size(),nullptr);
    r.model.execute(inputs.data(),static_cast<float*>(output)); return 0;
  } catch(const std::exception &e) { error=e.what(); return -1; }
}
void *q8b_thneed_load(cl_context context,cl_device_id device,cl_command_queue queue,const char *path,size_t output_bytes) {
  try {
    auto r=std::make_unique<Replay>(context,device,queue,nullptr);
    r->model.load(path);
    size_t size=0; check(clGetMemObjectInfo(r->model.output,CL_MEM_SIZE,sizeof(size),&size,nullptr));
    if(size!=output_bytes) throw std::runtime_error("output size mismatch");
    std::set<cl_mem> memory(r->model.input_clmem.begin(),r->model.input_clmem.end());
    std::set<cl_program> programs;
    memory.insert(r->model.output);
    for(auto &k:r->model.kq) {
      programs.insert(k->program);
      for(auto &a:k->args) if(a.size()==sizeof(cl_mem)) {
        cl_mem mem; std::memcpy(&mem,a.data(),sizeof(mem)); memory.insert(mem);
        cl_mem_object_type type=0; check(clGetMemObjectInfo(mem,CL_MEM_TYPE,sizeof(type),&type,nullptr));
        if(type!=CL_MEM_OBJECT_BUFFER) {
          cl_mem parent=nullptr; check(clGetImageInfo(mem,CL_IMAGE_BUFFER,sizeof(parent),&parent,nullptr));
          if(parent) memory.insert(parent);
        }
      }
    }
    r->memory.assign(memory.begin(),memory.end());r->programs.assign(programs.begin(),programs.end());
    return r.release();
  } catch(const std::exception &e) { error=e.what(); return nullptr; }
}
int q8b_thneed_upload(void *handle,unsigned index,const void *data,size_t size) {
  try {
    if(!handle || !data) throw std::runtime_error("invalid input");
    auto &r=*static_cast<Replay*>(handle);
    if(index>=r.model.input_clmem.size() || size!=r.model.input_sizes[index]) throw std::runtime_error("input size/index mismatch");
    check(clEnqueueWriteBuffer(r.model.command_queue,r.model.input_clmem[index],CL_TRUE,0,size,data,0,nullptr,nullptr));
    return 0;
  } catch(const std::exception &e) { error=e.what(); return -1; }
}
void q8b_thneed_destroy(void *handle) { delete static_cast<Replay*>(handle); }
}
