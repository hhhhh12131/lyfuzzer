import os
import re
import tkinter as tk
import utils
def prepare():
    # make clean
    os.system("rm -rf crash* fuzzer fuzzer.cc vulnerable_functions.h result corpus wrong_corpus")

    os.system("mkdir result corpus")
    # 将文本框1中的内容写入文件vulnerable_functions.h
    content1 = text1_user_fun.get(0.0, tk.END)    
    lines = content1.splitlines()
    cont2vulnerfile = ""
    for line in lines:
        if line.find('main') >= 0:
            break
        cont2vulnerfile += line + '\n'

    with open('vulnerable_functions.h', 'w') as f:
        f.write(cont2vulnerfile)


    global _variable_label
    _variable_label = 1
    # 根据文本框1中的函数生成接口函数,写入文件fuzzer.cc中
    content2 = utils.get_content2(content1)
    with open('fuzzer.cc', 'w') as f:
        f.write(content2)


import time


def fuzzing():
    starttime = time.time()
    os.system('clang++ -g -std=c++11 -fsanitize=address,fuzzer fuzzer.cc -o fuzzer')
    os.system('./fuzzer corpus/ > result/fuzzing_result.txt -max_len=1024 2>&1 -max_total_time=5')

    # 将fuzzing_result.txt文件的内容输出到文本框3中
    with open('result/fuzzing_result.txt') as f:
        content3 = f.read()
        text3_test_result.delete(0.0, tk.END)
        text3_test_result.insert(tk.INSERT, content3)
    endtime = time.time()
    if endtime - starttime > 5:
        str = 'ok,right, Your code is fine!'
        text3_test_result.insert(tk.INSERT, str)
        os.system('echo "\nok,right, Your code is fine!">>result/fuzzing_result.txt')

    os.system("cat crash* >> wrong_corpus")
    with open('wrong_corpus', 'rb') as f:
        wrong_corpus = f.read()
        text2.delete(0.0, tk.END)
        text2.insert(tk.INSERT, "错误语料为：\n")
        text2.insert(tk.INSERT, wrong_corpus)


def fuzzing_sim():
    # os.system('clang++ -g -std=c++11 -fsanitize=address,fuzzer fuzzer.cc -o fuzzer')
    # os.system('./fuzzer corpus/ -max_len=1024 -max_total_time=5 2>&1 | grep -E \'ERROR|#0|ok\' > result/fuzzing_result_sim.txt ')
    # os.system('./fuzzer > fuzzing_result_sim.txt 2>&1')
    os.system('cat result/fuzzing_result.txt | grep -E \'ERROR|#0|ok\' > result/fuzzing_result_sim.txt ')
    # 将fuzzing_result.txt文件的内容输出到文本框3中
    with open('result/fuzzing_result_sim.txt') as f:
        content3 = f.read()
        text3_test_result.delete(0.0, tk.END)
        text3_test_result.insert(tk.INSERT, content3)


file_path = ""

from tkinter import filedialog
def ask():
    global file_path
    file_path = filedialog.askopenfilename()
    print(file_path)
    with open(file_path, 'r') as f:
        content1 = f.read()
        text1_user_fun.delete(0.0, tk.END)
        text1_user_fun.insert(tk.INSERT, content1)

def save_file():
    # 打开文件保存对话框
    filepath = filedialog.asksaveasfilename(defaultextension='.txt' , initialfile='wrong_corpus.txt')
    if filepath:
        # 如果用户选择了路径，则将文件保存在指定路径
        with open('wrong_corpus', 'r') as file:
            content = file.read()
        with open(filepath, 'w') as file:
            file.write(content)
        
# ^_^ 添加主窗口(根窗口)
root_window = tk.Tk()

# ^_^ 根窗口配置
root_window.config(bg='#8DB6CD')  # 蓝色

# ^_^ 设置根窗口尺寸和位置

# 获取屏幕尺寸
screenwidth = root_window.winfo_screenwidth()
screenheight = root_window.winfo_screenheight()

# 设置窗口尺寸
width = screenwidth - 300
height = screenheight - 300

# 设置根窗口大小以及在屏幕中的位置
# geometry()方法的参数的四个数字分别代表窗口宽度,窗口高度,距离屏幕左侧距离,距离屏幕右侧距离
size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root_window.geometry(size_geo)

# ^_^ 标题
root_window.title('fuzzing tool V1.1')

# ^_^ 设置标签栏1和文本框1 接收用户函数
label1 = tk.Label(root_window, text="请在下方窗口输入将要进行模糊测试的用户函数:", font=("Arial", 10), fg="black", bg="#8DB6CD")
label1.grid(row=0, column=0, padx=10, pady=5)

text1_user_fun = tk.Text(root_window, undo=True, autoseparators=True, setgrid=True, wrap="word")
# width 一行可见的字符数；height 显示的行数
# 上述代码中 Text 控件通过 heigt 和 width 参数来控制文本域的大小（即纸张大小），当然也可以将其设置为自适用模式，即不设置具体的文本域大小
# 适用 pack(fill=X) 可以设置文本域的填充模式。比如 X表示沿水平方向填充，Y表示沿垂直方向填充，BOTH表示沿水平、垂直方向填充
text1_user_fun.grid(row=1, rowspan=3, column=0, padx=10, pady=5)

# ^_^ 设置标签栏2和文本框2 输出corpus
label2 = tk.Label(root_window, text="在此处显示错误语料", font=("Arial", 10), fg="black", bg="#8DB6CD")
label2.grid(row=4, column=1, padx=10, pady=5)

text2 = tk.Text(root_window, undo=True, autoseparators=True, setgrid=True, wrap="word")
# width 一行可见的字符数；height 显示的行数
# 上述代码中 Text 控件通过 heigt 和 width 参数来控制文本域的大小（即纸张大小），当然也可以将其设置为自适用模式，即不设置具体的文本域大小
# 适用 pack(fill=X) 可以设置文本域的填充模式。比如 X表示沿水平方向填充，Y表示沿垂直方向填充，BOTH表示沿水平、垂直方向填充
text2.grid(row=5, rowspan=2, column=1, padx=10, pady=5)


# ^_^ 设置标签栏3和文本框3 输出测试结果
label3 = tk.Label(root_window, text="模糊测试结果将在下方窗口中展示:", font=("Arial", 10), fg="black", bg="#8DB6CD")
label3.grid(row=0, column=1, padx=10, pady=5)

text3_test_result = tk.Text(root_window, undo=True, autoseparators=True, setgrid=True, wrap="word")
text3_test_result.grid(row=1, rowspan=3, column=1, padx=10, pady=5, sticky="NS")


# ^_^ Button控件 通过用户点击按钮的行为来执行回调函数，是 Button 控件的主要功用
# 按钮控件同样可以包含文本,图片,位图,应通过command参数执行回调函数(callback function)
# 当然Button也可以不绑定回调函数
bn_prepare = tk.Button(root_window,
                       text="     准  备     ", font=('微软雅黑', 10, 'bold'),
                       command=prepare).grid(row=1, column=3, padx=10, pady=5)

bn_fuzzing = tk.Button(root_window,
                       text="开始模糊测试", font=('微软雅黑', 10, 'bold'),
                       command=fuzzing).grid(row=2, column=3, padx=10, pady=5)

bn_fuzzing_sim = tk.Button(root_window,
                           text="生成关键信息", font=('微软雅黑', 10, 'bold'),
                           command=fuzzing_sim).grid(row=3, column=3, padx=10, pady=5)


bn_ask = tk.Button(root_window,
                    text="选择测试文件", font=('微软雅黑', 10, 'bold'),
                    command=ask).grid(row=0, column=3, padx=10, pady=5)

bn_sace=tk.Button(root_window,
                   text='保存错误语料', font=('微软雅黑', 10, 'bold'),
                   command=save_file).grid(row=4, column=3, padx=10, pady=5)

# ^_^ 通过主循环来显示窗口
root_window.mainloop()