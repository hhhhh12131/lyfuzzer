#include <stdint.h>
#include <stddef.h>
#include <cstring>

#include <array>
#include <string>
#include <vector>
//heap-buffer-overflow
bool t1(const uint8_t* data1, size_t size1, const uint8_t* data2, size_t size2) {
  bool result1 = false,result2=true;
  if (size1 >= 3) {
    result1 = data1[0] == 'F' &&
             data1[1] == 'U' &&
             data1[2] == 'Z' &&
             data1[3] == 'Z';
  }
  
  if (size2 >= 2) {
    result2 = data2[0] == 'M' &&
             data2[1] == 'Y' &&
             data2[2] == 'Z';
  }
  return result1&&result2;
}