#pragma once
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
namespace util {
inline std::string read_file(const char *path) {
  std::ifstream input(path,std::ios::binary);
  if(!input) throw std::runtime_error("Cannot open artifact");
  return std::string(std::istreambuf_iterator<char>(input),{});
}
}
