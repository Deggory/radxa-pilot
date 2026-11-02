#pragma once
#include <cstdint>
#include <ctime>
inline uint64_t nanos_since_boot() {
  timespec t{};
  clock_gettime(CLOCK_MONOTONIC, &t);
  return uint64_t(t.tv_sec) * 1000000000ULL + t.tv_nsec;
}
