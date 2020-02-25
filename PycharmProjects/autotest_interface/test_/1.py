"""
题目描述
计算字符串最后一个单词的长度，单词以空格隔开。
输入描述:

一行字符串，非空，长度小于5000。
输出描述:

整数N，最后一个单词的长度。

"""

in_str = input()
# print(len(in_str))
if in_str == '':
    print('输入为空')
elif len(in_str) > 5000:
    print('输入超过5000个字符')
else:
    in_list = in_str.split(' ')
    num = len(in_list)
    length = len(in_list[num-1])
    print(length)