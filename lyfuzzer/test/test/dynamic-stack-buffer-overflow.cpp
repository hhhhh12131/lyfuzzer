#include <stdint.h>
#include <stddef.h>
#include <cstring>

//dynamic-stack-buffer-overflow
bool t1(const uint8_t* data, size_t size, char* cbuf) {  
  cbuf[3]='a';
  bool result = false;
  if (size > 3) {
    result = data[0] == 'F' &&
             data[1] == 'U' &&
             data[2] == 'Z' &&
             data[3] == 'Z';
  }

  return result;
}