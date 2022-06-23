# -*- coding: utf-8 -*- 
# @Time : 2022/6/2 14:23 
# @Author : Daydreamer 
# @File : inner_function.py

"""
    Python 支持在函数内部定义函数，此类函数又称为局部函数
    和局部变量一样，默认情况下局部函数只能在其所在函数的作用域内使用
"""
# # 全局函数
# def out():
#     # 局部函数
#     def inner():
#         print("我是内部函数")
#     # 调用局部函数
#     inner()
# # 调用全局函数
# out()



"""
    通过将局部函数作为所在函数的返回值，可以扩大局部函数的使用范围
"""
def out():
    def inner():
        print("我是内部函数")
    return inner
receiver = out()
receiver()
