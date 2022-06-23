# -*- coding: utf-8 -*- 
# @Time : 2022/6/2 15:49 
# @Author : Daydreamer 
# @File : closure_test.py

"""
    闭包，又称闭包函数或者闭合函数，其实和前面讲的嵌套函数类似
    不同之处在于，闭包中外部函数返回的不是一个具体的值，而是一个函数。
    一般情况下，返回的函数会赋值给一个变量，这个变量可以在后面被继续执行调用
"""


def n_power(index):
    def calculate(number):
        return number ** index
    return calculate


square = n_power(2)     # 这里闭包的意义是会将自由变量 index 和 局部函数 calculate一起赋值给square 以保证能够进行计算
number = square(5)
print(number)
