# -*- coding: utf-8 -*-
# @Time : 2022/6/17 9:44
# @Author : Daydreamer
# @File : cumcount_test.py

"""
    cumcount:可对 Dataframe 进行分组排序生成排序列
"""

import pandas as pd

person_df = pd.DataFrame([['kangkang', 'male', 13, 89, 100, 96],
                          ['Maria', 'female', 13, 99, 98, 100],
                          ['Michael', 'male', 12, 60, 96, 100],
                          ['Jane', 'female', 11, 80, 88, 99]],
                         columns=['name', 'sex', 'age', 'chinese', 'math', 'english'])

"""
    select
        row_number() over(partition by sex order by chinese)
    from person
"""
# 方式一
# person_df['rk'] = person_df['chinese'].groupby(by=person_df['sex']).rank(ascending=False)

# 方式二
# 先排序 再分组 最后累加计数
person_df['chinese_rk'] = person_df.sort_values(by=['english'], ascending=False).groupby(by=['sex']).cumcount() + 1
print(person_df)
