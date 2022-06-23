# -*- coding: utf-8 -*- 
# @Time : 2022/6/7 9:36 
# @Author : Daydreamer 
# @File : redistest.py
"""
    redis的使用测试
"""

import redis
import pandas as pd

conn = redis.Redis(host='192.168.1.200', port=6379, db=0, password='Datayes@123')
# conn.set('name', 'Daydreamer')
# conn.hset(name='friend', key='best', value='Tiger')
# conn.hset(name='friend', key='normal', value='Fox')
# 'friend', ['KangKang', 'Maria', 'Michael', 'Jane']
# conn.lpush('Tools', 'asds', 'sddsa')
conn.lpop('Tools',2)
print(conn.get('name'))
