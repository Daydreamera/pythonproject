# coding=utf-8
import redis
import requests
import pandas as pd
from datetime import datetime
import time
import logging as logg
import config as conf
from DBConn import DBConn


def setup_logger(logger_name, log_file, level=logg.INFO):
    l = logg.getLogger(logger_name)
    formatter = logg.Formatter('%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s ')
    fileHandler = logg.FileHandler(log_file, mode='a', encoding='utf-8')
    fileHandler.setFormatter(formatter)
    streamHandler = logg.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)


def get_date(stime):
    start_year = int(stime.strftime('%Y')) - 2
    month_day = stime.strftime('%m-%d')
    start_time = str(start_year) + '-' + month_day + ' 00:00:00'
    end_time = stime.strftime('%Y-%m-%d %H:%M:%S')
    return start_time, end_time


def get_str(id_list):
    id_str = '('
    for data in id_list:
        id_str += "'" + str(data) + "',"
    id_str = id_str[:-1] + ')'
    return id_str


def direct_update(data_df):
    data_df['first_cover'] = 0
    data_df['first_cover_inst'] = 0
    data_df = data_df[name_var]
    insert_values = data_df.values.tolist()
    db_mysql.bulk_insert_mysql(conf.insert_roadshow_main_sql, insert_values)


def judge_is_cover(stime, sec_name, comp_hcode):
    """
    对每一条数据，判断是否首次覆盖和首次机构覆盖
    :param stime:
    :param sec_name:
    :param comp_hcode:
    :return:
    """
    start_time, end_time = get_date(stime)
    sec_df = all_df[(all_df['stime'] >= start_time) & (all_df['stime'] < end_time) &
                    (all_df['sec_name'] == sec_name)]
    if len(sec_df) == 0:
        first_cover = 1
    else:
        first_cover = 0

    if comp_hcode is None:
        first_cover_inst = 0
    else:
        comp_df = all_df[(all_df['stime'] >= start_time) & (all_df['stime'] < end_time) &
                         (all_df['sec_name'] == sec_name) & (all_df['comp_hcode'] == comp_hcode)]
        if len(comp_df) == 0:
            first_cover_inst = 1
        else:
            first_cover_inst = 0
    return first_cover, first_cover_inst


def judge_cover(data_df):
    """
    得到最后的dataframe
    :param data_df:
    :return:
    """
    all_values = []
    for _, row in data_df.iterrows():
        id = row['id']
        sec_name = row['sec_name']
        comp_hcode = row['comp_hcode']
        stime = row['stime']
        first_cover, first_cover_inst = judge_is_cover(stime, sec_name, comp_hcode)
        stime = stime.strftime('%Y-%m-%d %H:%M:%S')
        all_values.append([id, stime, first_cover, first_cover_inst])
    cover_df = pd.DataFrame(all_values, columns=name_var)
    cover_df.drop_duplicates(subset=name_var, keep='first', inplace=True)
    return cover_df


def get_insert_data(data_df):
    """
    最后的插入数据
    :param data_df:
    :return:
    """
    insert_data_list = []
    id_df = data_df[['id', 'stime']]
    id_df.drop_duplicates(subset=['id', 'stime'], keep='first', inplace=True)
    id_list = id_df.values.tolist()
    for id, stime in id_list:
        one_data_df = data_df[(data_df['id'] == id) & (data_df['stime'] == stime)]
        if len(one_data_df) == 1:
            data_list = one_data_df.values.tolist()
            insert_data_list.append(data_list[0])
        else:
            if len(one_data_df[one_data_df['first_cover'] == 1]) > 0:
                first_cover = 1
            else:
                first_cover = 0
            if len(one_data_df[one_data_df['first_cover_inst'] == 1]) > 0:
                first_cover_inst = 1
            else:
                first_cover_inst = 0
            insert_data_list.append([id, stime, first_cover, first_cover_inst])
    db_mysql.bulk_insert_mysql(conf.insert_roadshow_main_sql, insert_data_list)


def get_all_data(data_df):
    """
    获取路演和个股的对应情况，而不是sec_json
    :param data_df:
    :return:
    """
    real_data_list = []
    for _, row in data_df.iterrows():
        id = row['id']
        sec_json = row['sec_json']
        comp_hcode = row['comp_hcode']
        stime = row['stime']
        sec_dict = eval(sec_json)
        for sec_hcode, sec_name in sec_dict.items():
            real_data_list.append([id, stime, sec_name, comp_hcode])
    real_df = pd.DataFrame(real_data_list, columns=['id', 'stime', 'sec_name', 'comp_hcode'])
    real_df.drop_duplicates(subset=['id', 'stime', 'sec_name', 'comp_hcode'], keep='first', inplace=True)
    return real_df


def get_data():
    is_sql = """
                select 
                    id,
                    sec_json,
                    sec_name,
                    comp_hcode,
                    stime 
                from app_research_service.ROADSHOW_MAIN 
                where sec_json is not null 
                and hcreatetime>='{last_updatetime}'
    """.format(last_updatetime=conf.last_update_updatetime)
    data_df = db_mysql.get_sql_result_pd(is_sql)
    # 把sec_json全部拆成独立的sec_name
    real_df = get_all_data(data_df)
    # 单独判断每条是否覆盖
    cover_df = judge_cover(real_df)
    # 然后根据每条是否覆盖的情况去更新一条路演是否真正覆盖
    get_insert_data(cover_df)

    # 对于sec_json为空的数据直接更新
    not_sql = """
    select id,sec_json,sec_name,stime from app_research_service.ROADSHOW_MAIN where sec_json
    is null and hupdatetime>='{last_updatetime}'
    """.format(last_updatetime=conf.last_update_updatetime)
    not_data_df = db_mysql.get_sql_result_pd(not_sql)
    not_data_df['stime'] = not_data_df['stime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    direct_update(not_data_df)


if __name__ == '__main__':
    db_mysql = DBConn(dbtype='mysql', host=conf.db_server, port=conf.db_port, user=conf.username,
                      passwd=conf.password, dbname=conf.dbname)

    log_filename = conf.LOG_PATH
    setup_logger('log', log_filename)
    logg = logg.getLogger('log')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    all_df = get_all_data(db_mysql.get_sql_result_pd(conf.all_data_sql))
    all_df['stime'] = all_df['stime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    name_var = ['id', 'stime', 'first_cover', 'first_cover_inst']

    get_data()
    with open(conf.UPDATE_TIME_PATH, 'w') as f:
        f.write(current_time)



