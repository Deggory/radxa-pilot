// Small Linux UVC MMAP capture helper. Preserves kernel timestamps and sequence IDs.
#include <errno.h>
#include <fcntl.h>
#include <linux/videodev2.h>
#include <poll.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <unistd.h>

struct capture {
  int fd, streaming, saved;
  int last_read_error;
  int dynamic_framerate_saved, old_dynamic_framerate;
  unsigned count;
  struct v4l2_format fmt;
  struct v4l2_streamparm parm;
  void *maps[8];
  size_t sizes[8];
  struct v4l2_format old_fmt;
  struct v4l2_streamparm old_parm;
};
// 0=none, 1=poll, 2=device event, 3=dequeue, 4=invalid index,
// 5=invalid payload size, 6=driver marked buffer ERROR,
// 7=non-monotonic timestamp, 8=requeue.
int camera_last_read_error(struct capture *c) { return c ? c->last_read_error : 0; }
static int xioctl(int fd, unsigned long req, void *arg) {
  int r;
  do { r = ioctl(fd, req, arg); } while (r == -1 && errno == EINTR);
  return r;
}
void camera_close(struct capture *c) {
  if (!c) return;
  if (c->fd >= 0) {
    enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    if (c->streaming) xioctl(c->fd, VIDIOC_STREAMOFF, &type);
    for (unsigned i=0; i<c->count; i++)
      if (c->maps[i] && c->maps[i] != MAP_FAILED) munmap(c->maps[i], c->sizes[i]);
    struct v4l2_requestbuffers req = {.type=type, .memory=V4L2_MEMORY_MMAP};
    if (c->saved) xioctl(c->fd, VIDIOC_REQBUFS, &req);
    if (c->saved) {
      xioctl(c->fd, VIDIOC_S_FMT, &c->old_fmt);
      xioctl(c->fd, VIDIOC_S_PARM, &c->old_parm);
    }
    if (c->dynamic_framerate_saved) {
      struct v4l2_control ctrl = {.id=V4L2_CID_EXPOSURE_AUTO_PRIORITY, .value=c->old_dynamic_framerate};
      xioctl(c->fd, VIDIOC_S_CTRL, &ctrl);
    }
    close(c->fd);
  }
  free(c);
}
struct capture *camera_open_ex(const char *path, unsigned width, unsigned height, unsigned fps,
                               uint32_t pixel_format, unsigned buffer_count) {
  if (buffer_count < 2 || buffer_count > 8 || !fps) { errno=EINVAL; return NULL; }
  struct capture *c = calloc(1, sizeof(*c));
  if (!c) return NULL;
  c->fd = open(path, O_RDWR | O_NONBLOCK | O_CLOEXEC);
  if (c->fd < 0) goto fail;
  struct v4l2_capability cap = {0};
  if (xioctl(c->fd, VIDIOC_QUERYCAP, &cap) < 0) goto fail;
  if (strcmp((char *)cap.driver, "uvcvideo")) { errno=ENODEV; goto fail; }
  c->old_fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
  c->old_parm.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
  if (xioctl(c->fd, VIDIOC_G_FMT, &c->old_fmt) < 0 || xioctl(c->fd, VIDIOC_G_PARM, &c->old_parm) < 0) goto fail;
  c->saved = 1;
  // Same fixed-cadence policy used by the qualified AK-Camera tests. Automatic
  // exposure can otherwise slow a negotiated 60 Hz stream down in low light.
  // Save/restore this one control; do not set shutter, gain, focus or clocks.
  struct v4l2_control ctrl = {.id=V4L2_CID_EXPOSURE_AUTO_PRIORITY};
  if (xioctl(c->fd, VIDIOC_G_CTRL, &ctrl) < 0) goto fail;
  c->old_dynamic_framerate=ctrl.value;
  c->dynamic_framerate_saved=1;
  ctrl.value=0;
  if (xioctl(c->fd, VIDIOC_S_CTRL, &ctrl) < 0) goto fail;
  c->fmt.type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
  c->fmt.fmt.pix.width=width; c->fmt.fmt.pix.height=height;
  c->fmt.fmt.pix.pixelformat=pixel_format; c->fmt.fmt.pix.field=V4L2_FIELD_ANY;
  if (xioctl(c->fd, VIDIOC_S_FMT, &c->fmt) < 0) goto fail;
  if (c->fmt.fmt.pix.width != width || c->fmt.fmt.pix.height != height || c->fmt.fmt.pix.pixelformat != pixel_format) {
    errno=EINVAL; goto fail;
  }
  c->parm.type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
  c->parm.parm.capture.timeperframe.numerator=1; c->parm.parm.capture.timeperframe.denominator=fps;
  if (xioctl(c->fd, VIDIOC_S_PARM, &c->parm) < 0) goto fail;
  struct v4l2_requestbuffers req = {.count=buffer_count, .type=V4L2_BUF_TYPE_VIDEO_CAPTURE, .memory=V4L2_MEMORY_MMAP};
  if (xioctl(c->fd, VIDIOC_REQBUFS, &req) < 0) goto fail;
  if (req.count < 2 || req.count > 8) { errno=ENOMEM; goto fail; }
  c->count=req.count;
  for (unsigned i=0; i<c->count; i++) {
    struct v4l2_buffer b = {.type=req.type, .memory=req.memory, .index=i};
    if (xioctl(c->fd, VIDIOC_QUERYBUF, &b) < 0) goto fail;
    c->sizes[i]=b.length;
    c->maps[i]=mmap(NULL, b.length, PROT_READ | PROT_WRITE, MAP_SHARED, c->fd, b.m.offset);
    if (c->maps[i] == MAP_FAILED || xioctl(c->fd, VIDIOC_QBUF, &b) < 0) goto fail;
  }
  enum v4l2_buf_type type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
  if (xioctl(c->fd, VIDIOC_STREAMON, &type) < 0) goto fail;
  c->streaming=1;
  return c;
fail: ;
  int saved_errno=errno;
  camera_close(c); errno=saved_errno; return NULL;
}

struct capture *camera_open(const char *path, unsigned width, unsigned height, unsigned fps) {
  return camera_open_ex(path, width, height, fps, V4L2_PIX_FMT_MJPEG, 4);
}

// info: width, height, fourcc, fps numerator, fps denominator, buffer count, sizeimage.
int camera_get_info(struct capture *c, uint32_t info[7]) {
  if (!c || !info) { errno=EINVAL; return -1; }
  info[0]=c->fmt.fmt.pix.width; info[1]=c->fmt.fmt.pix.height;
  info[2]=c->fmt.fmt.pix.pixelformat;
  info[3]=c->parm.parm.capture.timeperframe.denominator;
  info[4]=c->parm.parm.capture.timeperframe.numerator;
  info[5]=c->count; info[6]=c->fmt.fmt.pix.sizeimage;
  return 0;
}
// meta: monotonic timestamp ns, sequence, flags, number of older queued frames discarded.
int camera_read(struct capture *c, unsigned char *dst, unsigned capacity, uint64_t meta[4]) {
  c->last_read_error=0;
  struct pollfd p={.fd=c->fd, .events=POLLIN};
  int r;
  do { r=poll(&p, 1, 3000); } while (r<0 && errno==EINTR);
  if (r<=0) { c->last_read_error=1; if (!r) errno=ETIMEDOUT; return -1; }
  if (p.revents & (POLLERR | POLLHUP | POLLNVAL)) { c->last_read_error=2; errno=ENODEV; return -1; }
  int bytes=-1;
  unsigned dequeued=0;
  struct v4l2_buffer newest={0};
  int have_newest=0;
  for (unsigned i=0; i<c->count; i++) {
    struct v4l2_buffer b={.type=V4L2_BUF_TYPE_VIDEO_CAPTURE, .memory=V4L2_MEMORY_MMAP};
    if (xioctl(c->fd, VIDIOC_DQBUF, &b)<0) {
      if (errno==EAGAIN && have_newest) break;
      c->last_read_error=3;
      int saved_errno=errno;
      if (have_newest) xioctl(c->fd, VIDIOC_QBUF, &newest);
      errno=saved_errno;
      return -1;
    }
    int valid=b.index<c->count && b.bytesused<=capacity && b.bytesused>0 &&
      b.bytesused<=c->sizes[b.index] && !(b.flags & V4L2_BUF_FLAG_ERROR) &&
      (b.flags & V4L2_BUF_FLAG_TIMESTAMP_MASK)==V4L2_BUF_FLAG_TIMESTAMP_MONOTONIC;
    if (!valid) {
      c->last_read_error=b.index>=c->count ? 4 :
        (b.bytesused>capacity || b.bytesused==0 || b.bytesused>c->sizes[b.index]) ? 5 :
        (b.flags & V4L2_BUF_FLAG_ERROR) ? 6 : 7;
      int bad_requeue_failed=xioctl(c->fd, VIDIOC_QBUF, &b)<0;
      int newest_requeue_failed=have_newest && xioctl(c->fd, VIDIOC_QBUF, &newest)<0;
      if (bad_requeue_failed || newest_requeue_failed) {
        c->last_read_error=8;
        return -1;
      }
      errno=EIO; return -1;
    }
    if (have_newest && xioctl(c->fd, VIDIOC_QBUF, &newest)<0) {
      c->last_read_error=8;
      int saved_errno=errno;
      xioctl(c->fd, VIDIOC_QBUF, &b);
      errno=saved_errno;
      return -1;
    }
    newest=b; have_newest=1; dequeued++;
  }
  if (!have_newest) { errno=EAGAIN; return -1; }
  memcpy(dst, c->maps[newest.index], newest.bytesused); bytes=(int)newest.bytesused;
  meta[0]=(uint64_t)newest.timestamp.tv_sec*1000000000ull+(uint64_t)newest.timestamp.tv_usec*1000;
  meta[1]=newest.sequence; meta[2]=newest.flags; meta[3]=dequeued-1;
  if (xioctl(c->fd, VIDIOC_QBUF, &newest)<0) { c->last_read_error=8; return -1; }
  return bytes;
}
