# -*- coding: utf-8 -*- 
# @Time : 2022/6/7 17:10 
# @Author : Daydreamer 
# @File : decorator_args_test.py


"""
    测试装饰器和被装饰函数分别带函数的情况
"""

import datetime


# 被装饰的函数带参
def timelog(func):
    def wrapper(*args, **kwargs):
        print(datetime.datetime.now())
        res = func(*args, **kwargs)
        print(datetime.datetime.now())
        return res
    return wrapper


@timelog
def run(a, b):
    return a + b


# print(run(b=1, a=2))


# 装饰器带参数
def wrapper_out(parameter):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            username = input('请输入用户名：').strip()
            password = input('请输入密码：').strip()
            # 注意文件名需要与装饰器传入参数一致，增强耦合性思想
            with open(parameter, encoding='utf-8', mode='r') as f:
                for line in f:
                    user, pwd = line.strip().split('|')
                    if user == username and pwd == password:
                        ret = func(*args, **kwargs)
                        return ret
                return False
        return _wrapper
    return wrapper


@wrapper_out('wechat')  # 此处的wrapper_out是带了()的  可以理解为已经执行的函数 所以装饰wechat()的是wrapper()函数
def wechat():
    print('成功登录微信！')


wechat()
