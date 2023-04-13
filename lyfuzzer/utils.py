import re

# 从函数定义中获取函数名字符串
def func_definition_line2funname(line):
    right = line.find('(') - 1
    while line[right] == ' ':
        right -= 1

    left = right
    while left >= 0 and line[left] != ' ':
        left -= 1

    return line[left + 1:right + 1]


# 从函数定义行中获取括号中间的字符串列表,会清除两端多余的空格
def func_definition_line2type_var_list(line):
    left = line.find('(') + 1
    right = line.find(')') - 1

    # 去除左边的空格
    arguments_length = right - left + 1
    for i in range(arguments_length):
        if line[left] == ' ':
            left += 1
        else:
            break

    # 去除右边的空格
    arguments_length = right - left + 1
    for i in range(arguments_length):
        if line[right] == ' ':
            right -= 1
        else:
            break

    all_type_var = line[left:right + 1]

    if len(all_type_var) == 0 or all_type_var == 'void':
        return []

    all_type_var = re.sub(' +', ' ', all_type_var, 0)
    all_type_var = re.sub(r' +\*', '*', all_type_var, 0)
    type_var_list = re.split(" *, *", all_type_var)
    return type_var_list


# 从"int pos"中获取pos字符串,默认参数type_var两侧没有多余空格且不为空,返回的字符串两侧也没有多余空格
def type_var2var(type_var):
    left = len(type_var) - 1
    if type_var[left] != ' ':
        left -= 1
    return type_var[left + 1:len(type_var)]


def content2func_definition_line_list(content1):
    line = ""
    list = []
    lines = content1.splitlines()
    for line in lines:
        if re.match('^\s*(\w+(?:\s*\*\s*)?)\s+(\w+)\s*\((.*)\)\s*', line):
            if line.find('main') >= 0:
                break
            list.append(line)
    return list


def type_var_list2content2_varpart(type_var_list, funname):
    # 提供精细化,可定制化的模糊测试

    global _variable_label
    content2_funinvoke = '\t' + funname + '('
    content2_randomvariable = "\n\t// 以下为程序生成的代码：\n"
    # 如果用户指定了byte数组和size这两个变量
    # 如果用户不指定, 默认char*为字符串指针,以'\0'结尾

    i = 0
    while i < len(type_var_list):
        argument = type_var_list[i]
        print(argument)
        # e.g.: argument = 'int* abc' # 此处的argument默认只有一个空格，前面已经实现
        # argument = re.sub(' +', ' ', argument, 0)

        # 把用户指定的那两个放在最前面
        # if
        # elif
        if (ob := re.match(r"((const )?uint8_t|((unsigned )?(byte|unsigned char)))\*",
                           argument)) is not None:  # const uint8_t *
            content2_funinvoke += '(' + ob.group() + ')data, '
            # byte* 默认要指定字节块长度
            # (byte* buf, int len)
            i += 1
            ob1 = re.match("byte|short|int|long|size_t", type_var_list[i])
            type = ob1.group()
            if type == 'byte':
                content2_randomvariable += '\tbyte _value_fuzzing' + str(_variable_label) + ' = size%INT8_MAX;\n'
                content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
                _variable_label += 1

            elif type == 'short':
                content2_randomvariable += '\tshort _value_fuzzing' + str(_variable_label) + ' = size%INT16_MAX;\n'
                content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
                _variable_label += 1

            elif type == 'int':
                content2_randomvariable += '\tint _value_fuzzing' + str(_variable_label) + ' = size%INT32_MAX;\n'
                content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
                _variable_label += 1

            elif type == 'long':
                content2_randomvariable += '\tlong _value_fuzzing' + str(_variable_label) + ' = size%INT64_MAX;\n'
                content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
                _variable_label += 1

            elif type == 'size_t':
                content2_funinvoke += 'size, '
            print(type_var_list[i])


        # char* 默认不用指定长度，使用'\0'
        elif (ob := re.match(r"(const )?(unsigned )?char ?\*", argument)) is not None:  # const uint8_t *
            content2_randomvariable += '\tchar cbuffer' + str(_variable_label) + '[size+1];\n' \
                                                                                 '\tmemcpy(cbuffer' + str(
                _variable_label) + ', data, size);\n' \
                                   "\tcbuffer" + str(_variable_label) + "[size] = '\\0';\n"
            content2_funinvoke += '(' + ob.group() + ')cbuffer' + str(_variable_label) + ', '
            _variable_label += 1


        # 常见数据类型指针 默认为int* ,而不是int *
        elif (ob := re.match(r'(unsigned )?(byte|short|int|long|float|double)\*', argument)) is not None:
            # e.g.: unsigned int*
            datatype = ob.group()

            # e.g. unsigned int _value_fuzzing1 = (unsigned int) dist_unsigned_int(rng);
            #      unsigned int* _value_fuzzing2 = & _value_fuzzing1;
            content2_randomvariable += '\t' + datatype.replace('*', '') + ' _value_fuzzing' + str(_variable_label) + \
                                       ' = (' + datatype.replace('*', '') + ') dist_' + \
                                       datatype.replace(' ', '_').replace('*', '') + '(rng);\n'

            content2_randomvariable += '\t' + datatype + ' _value_fuzzing' + str(_variable_label + 1) + \
                                       ' = &_value_fuzzing' + str(_variable_label) + ';\n'

            content2_funinvoke += '_value_fuzzing' + str(_variable_label + 1) + ', '
            _variable_label += 2

        elif argument[0:5] == 'float':
            content2_randomvariable += '\tfloat _value_fuzzing' + str(_variable_label) + ' = (float) dist_float(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        elif argument[0:6] == 'double':
            content2_randomvariable += '\tdouble _value_fuzzing' + str(_variable_label) + \
                                       ' = (double) dist_double(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        elif argument[0:4] == 'bool':
            content2_randomvariable += '\tbool _value_fuzzing' + str(_variable_label) + \
                                       ' = dist_byte(rng)%2 == 0 ? true : false;\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1
        elif argument[0:4] == 'char':
            content2_randomvariable += '\tchar _value_fuzzing' + str(_variable_label) + \
                                       ' = (char) dist_char(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        elif argument[0:3] == 'int':
            content2_randomvariable += '\tint _value_fuzzing' + str(_variable_label) + \
                                       ' = (int) dist_int(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        elif argument[0:4] == 'long':
            content2_randomvariable += '\tlong _value_fuzzing' + str(_variable_label) + \
                                       ' = (long) dist_long(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        elif argument[0:5] == 'short':
            content2_randomvariable += '\tshort _value_fuzzing' + str(_variable_label) + \
                                       ' = (short) dist_short(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        elif argument[0:4] == 'byte':
            content2_randomvariable += '\tbyte _value_fuzzing' + str(_variable_label) + \
                                       ' = (byte) dist_byte(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        elif argument[0:12] == 'unsigned int':
            content2_randomvariable += '\tunsigned int _value_fuzzing' + str(_variable_label) + \
                                       ' = (unsigned int) dist_unsigned_int(rng);\n'
            content2_funinvoke += '_value_fuzzing' + str(_variable_label) + ', '
            _variable_label += 1

        i += 1

    content2_funinvoke = content2_funinvoke[0:len(content2_funinvoke) - 2]
    content2_funinvoke += ');\n\n'

    return content2_randomvariable + content2_funinvoke


_variable_label = 1


def get_content2(content1):
    lines = content2func_definition_line_list(content1)
    content2_varpart = ""

    for line in lines:
        # e.g.  line = 'bool test1(   const uint8_t* pp, size_t len,   bool b, float  f  )'
        funname = func_definition_line2funname(line)  # 去除了两侧的多余空格
        type_var_list = func_definition_line2type_var_list(line)  # 规范的list,去除了多余的空格
        if len(type_var_list) == 0:
            # 以弹窗的形式展示出来
            print("该函数没有参数,无法进行测试")  # ????
        content2_varpart += type_var_list2content2_varpart(type_var_list, funname)

    content2_headerfile = '#include <stddef.h>\n' \
                          '#include <stdint.h>\n' \
                          '#include <random>\n' \
                          '#include <cstring>\n' \
                          '#include "vulnerable_functions.h"\n' \
                          'using namespace std;\n' \
                          '\nextern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {\n\n'

    content2_randomgener = '\t// 创建一个随机数引擎\n' \
                           '\tmt19937 rng(random_device{}());\n' \
                           '\t// 创建一个分布，指定要生成的随机数范围\n' \
                           '\t// 整型\n' \
                           '\tuniform_int_distribution<int> dist_byte(INT8_MIN, INT8_MAX);\n' \
                           '\tuniform_int_distribution<int> dist_unsigned_byte(0, UINT8_MAX);\n' \
                           '\tuniform_int_distribution<int> dist_short(INT16_MIN, INT16_MAX);\n' \
                           '\tuniform_int_distribution<int> dist_unsigned_short(0, UINT16_MAX);\n' \
                           '\tuniform_int_distribution<int> dist_int(INT32_MIN, INT32_MAX);\n' \
                           '\tuniform_int_distribution<int> dist_unsigned_int(0, UINT32_MAX);\n' \
                           '\tuniform_int_distribution<long> dist_long(INT64_MIN, INT64_MAX);\n' \
                           '\tuniform_int_distribution<long> dist_unsigned_long(0, UINT64_MAX);\n' \
                           '\t// 浮点型\n' \
                           '\tuniform_real_distribution<double> dist_float(-3.40E+38, 3.40E+38);\n' \
                           '\tuniform_real_distribution<double> dist_double(-1.79E+308, 1.79E+308);\n' \
                           '\t//char\n' \
                           '\tuniform_int_distribution<int> dist_char(-128,127);\n'

    content2_lastpart = "\treturn 0;\n}\n"

    return content2_headerfile + content2_randomgener + content2_varpart + content2_lastpart





