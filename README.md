# lyfuzzer
a demo combining libfuzzer with good GUI to detect C/C++code
### 功能说明
目前可检测的漏洞类型/源代码包括：
1.按错误分类
（1）dynamic-stack-buffer-overflow

（2）heap-buffer-overflow

（3）SEGV on unknown address

（4）stack-buffer-overflow

（5）memory-leaks

2.程序员常犯错误
（1）指针非法访问

（2）数组访问越界

3.头文件
4.其他
（1）包含各种常见类型参数的函数

（2）嵌入式开发中的函数

（3）计算机网络开发中的函数

（4）正常的函数

### demo运行
1.linux环境安装libfuzzer，详见[libfuzzer官方文档](https://github.com/Dor1s/libfuzzer-workshop "libfuzzer官方文档")
2.终端中输入 `python3 main.py`即可。
3.先选择直接贴入源码或者选择文件，在点击依次“准备”、“开始模糊测试”；
4.“生成关键信息”可以生成简要的报错代码
5.最后可以保存可能的错误语料到指定的代码。
可选择test文件夹中的例子作为演示。
### demo截图
[![image.png](https://i.postimg.cc/QCvLtpHP/image.png)](https://postimg.cc/T5jNN5jq)

注：目前代码完善度不够，还需修改。




###Function Description

The types of vulnerabilities/source code that can be detected currently include:

1.Classification by Error

（1）dynamic-stack-buffer-overflow

（2）heap-buffer-overflow

（3）SEGV on unknown address

（4）stack-buffer-overflow

（5）memory-leaks

2.Programmers often make mistakes

(1) Illegal pointer access

(2) Array access out of bounds

3.Header file

4.Others

(1) Functions containing various common types of parameters

(2) Functions in embedded development

(3) Functions in Computer Network Development

(4) Normal function

###Demo

1.Install libfuzzer in the Linux environment, please refer to [official document of libfuzzer](https://github.com/Dor1s/libfuzzer-workshop "official document of libfuzzer") for details

2.Enter `python3 main.py` in the terminal.

3.First, choose to directly paste the source code or select a file, and then click on "Prepare" and then "Start Fuzzy Testing";

4.'Generate Key Information' can generate brief error codes

5.Finally, possible incorrect corpus can be saved to the specified code.

You can choose the example in the test folder as a demonstration.

###Demo screenshot

[![image.png]( https://i.postimg.cc/QCvLtpHP/image.png )]( https://postimg.cc/T5jNN5jq )



Note: Currently, the code is not complete enough and needs to be modified.
