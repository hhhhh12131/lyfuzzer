#include <stdint.h>
#include <stddef.h>
#include <cstring>
#include <array>
#include <string>
#include <vector>
//heap-buffer-overflow
int t2(uint8_t* data, int size) {
  bool result = false;
  if (size >= 3) {
    result = data[0] == 'F' &&
             data[1] == 'U' &&
             data[2] == 'Z' &&
             data[3] == 'Z';
  }

  return (int)result;
}