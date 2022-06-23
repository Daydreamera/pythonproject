# -*- coding: utf-8 -*- 
# @Time : 2022/6/7 15:44 
# @Author : Daydreamer 
# @File : globals_test.py

a = 100  # 定义全局变量


def test1():
    print(a)  # 函数内部引用全局变量没有问题


# def test2():
#     a += 1
#     print(a)        # 函数内部修改全局变量报错

def test3():
    global a
    a += 1
    print(a)  # 使用global关键字之后再修改全局变量不报错


if __name__ == '__main__':
    test1()
    test3()
