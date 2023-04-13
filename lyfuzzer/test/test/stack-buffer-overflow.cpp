#include <stdint.h>
#include <stddef.h>
#include <cstring>

#include <array>
#include <string>
#include <vector>
//stack-buffer-overflow
double t4(const uint8_t* data, size_t size,int *arr) {
  bool result = false;
  if (size > 3) {
    result = data[0] == 'F' &&
             data[1] == 'U' &&
             data[2] == 'Z' &&
             data[3] == 'Z';
  }
  arr[4]=5;
  return (double)result;
}