#pragma once
#include <CL/cl.h>
#include <cassert>
#include <string>
// Minimal support for unchanged portable Thneed sources; select a GPU only.
#define CL_CHECK(expr) do { assert(CL_SUCCESS == (expr)); } while (0)
#define CL_CHECK_ERR(expr) ({ cl_int err=CL_INVALID_VALUE; auto ret=(expr); assert(ret && err==CL_SUCCESS); ret; })
cl_device_id cl_get_device_id(cl_device_type type);
const char *cl_get_error_string(int error);
cl_program cl_program_from_source(cl_context context,cl_device_id device,const std::string &source);
cl_program cl_program_from_binary(cl_context context,cl_device_id device,const uint8_t *binary,size_t size);
