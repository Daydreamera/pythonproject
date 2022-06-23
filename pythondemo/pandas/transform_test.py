# -*- coding: utf-8 -*- 
# @Time : 2022/6/10 13:41 
# @Author : Daydreamer 
# @File : transform_test.py

import pandas as pd

person_df = pd.DataFrame([['kangkang', 'male', 13, 89, 100, 96],
                          ['Maria', 'female', 13, 99, 98, 100],
                          ['Michael', 'male', 12, 60, 96, 100],
                          ['Jane', 'female', 11, 80, 88, 99]],
                         columns=['name', 'sex', 'age', 'chinese', 'math', 'english'])

print(person_df)
print("=" * 100)
person_df['avg_chinese'] = person_df.groupby(by='sex')['chinese'].transform('mean')
person_df['avg_math'] = person_df.groupby(by='sex')['math'].transform('mean')
person_df['avg_english'] = person_df.groupby(by='sex')['english'].transform('mean')
print(person_df)