#include <stdio.h>
#include <stdint.h>
#include <string.h>
//计算机网络中接收一个数据包的指针和大小，并将其存储在本地缓冲区中
//stack-buffer-overflow 
void process_packet(const uint8_t* packet, size_t size) {
 char buffer[256];
 memset(buffer, 0, sizeof(buffer));
 memcpy(buffer, packet, size);//memcpy函数将数据包复制到缓冲区中
                            //数据包的大小大于缓冲区大小，发生堆栈溢出

}

int main() {
 uint8_t packet[] = {0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x2C, 0x20, 0x77, 0x6F, 0x72, 0x6C, 0x64, 0x21};
 process_packet(packet, sizeof(packet));
 return 0;
}