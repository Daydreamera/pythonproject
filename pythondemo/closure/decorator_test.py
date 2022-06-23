# -*- coding: utf-8 -*- 
# @Time : 2022/6/7 15:59 
# @Author : Daydreamer 
# @File : decorator_test.py

"""
    设计一个统计程序执行耗时的程序
"""
import time


def run():
    add_sum = 0
    for i in range(1000000000):
        add_sum += i
    return add_sum


# 常规做法
# 缺点：改变了执行函数的调用方式 run() --> time_count(run)
def time_count(func):
    stime = time.time()
    s = func()
    etime = time.time()
    print('程序耗时：', (etime - stime))
    return s


# print(time_count(run))

# 使用装饰器
def timecount(func):
    def wrapper():
        stime = time.time()
        s = func()
        etime = time.time()
        print('程序耗时：', (etime - stime))
        return s

    return wrapper


# run = timecount(run)
# print(run())

# # @的工作原理是：将下方被装饰函数的函数名作为参数传给装饰器，把装饰器的返回值赋值给被装饰的函数名
@timecount
def printf():
    print('打印一句话')

printf()