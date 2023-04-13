#include <stdint.h>
#include <stddef.h>
#include <cstring>

//SEGV on unknown address
double t4(const uint8_t* data, size_t size,int *arr ,int num) {
  int sum = 0;
  for(int i = 0;i < size; i++)
  {
    sum += (int)data[i];
  }
  arr[num+1]=sum;
}