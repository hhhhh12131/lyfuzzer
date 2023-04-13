#include <stddef.h>
#include <stdint.h>
#include <random>
#include <cstring>
#include "vulnerable_functions.h"
using namespace std;

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {

	// ����һ�����������
	mt19937 rng(random_device{}());
	// ����һ���ֲ���ָ��Ҫ���ɵ��������Χ
	// ����
	uniform_int_distribution<int> dist_byte(INT8_MIN, INT8_MAX);
	uniform_int_distribution<int> dist_unsigned_byte(0, UINT8_MAX);
	uniform_int_distribution<int> dist_short(INT16_MIN, INT16_MAX);
	uniform_int_distribution<int> dist_unsigned_short(0, UINT16_MAX);
	uniform_int_distribution<int> dist_int(INT32_MIN, INT32_MAX);
	uniform_int_distribution<int> dist_unsigned_int(0, UINT32_MAX);
	uniform_int_distribution<long> dist_long(INT64_MIN, INT64_MAX);
	uniform_int_distribution<long> dist_unsigned_long(0, UINT64_MAX);
	// ������
	uniform_real_distribution<double> dist_float(-3.40E+38, 3.40E+38);
	uniform_real_distribution<double> dist_double(-1.79E+308, 1.79E+308);
	//char
	uniform_int_distribution<int> dist_char(-128,127);

	// ����Ϊ�������ɵĴ��룺
	int _value_fuzzing1 = size%INT32_MAX;
	t2((uint8_t*)data, _value_fuzzing1);

	return 0;
}
