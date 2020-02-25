"""
题目描述
写出一个程序，接受一个由字母和数字组成的字符串，和一个字符，然后输出输入字符串中含有该字符的个数。不区分大小写。

输入描述:

第一行输入一个有字母和数字以及空格组成的字符串，第二行输入一个字符。
输出描述:

输出输入字符串中含有该字符的个数。

"""

str1 = input("输入第一行字符串：").lower()
str2 = input("输入查找字符：").lower()
print(str1.count(str2))


# def aaa(sss):
#     for i in sss:
#         if i.isalnum() or i.isspace():
#             return i
#         else:
#             return i
#
#
# str1 = input("输入第一行字符串：").lower()
#
# print(aaa(str1))
#
# if aaa(str1):
#     str2 = input("输入查找字符：").lower()
#     n = 0
#     for i in str1:
#         if i == str2:
#             n = n + 1
#     print(n)
# else:
#     print()


