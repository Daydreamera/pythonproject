# -*- coding: utf-8 -*- 
# @Time : 2022/6/7 15:51 
# @Author : Daydreamer 
# @File : nonlocal_test.py


def outer():
    a = 100
    def inner():
        nonlocal a      # nonlocal声明的变量不是局部变量,也不是全局变量,而是外部嵌套函数内的变量
        a += 1
        return a
    return inner

out = outer()
print(out())
print(out())
print(out())