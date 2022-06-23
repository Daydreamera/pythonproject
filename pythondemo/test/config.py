# coding=utf-8
import os
from datetime import datetime, timedelta

# 讯兔正式库
db_server = 'prd-rabyte-data.cmz9yspwe5fc.rds.cn-northwest-1.amazonaws.com.cn'
username = 'root'
password = 'WBwUvMyakdpP8uOW492t'
dbname = 'esg_analytics'
db_port = '3306'

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_LOG_PATH = os.path.join(BASE_PATH, 'logs')
now = datetime.now().strftime('%Y-%m-%d')
LOG_PATH = os.path.join(FILE_LOG_PATH, str(now) + '.log')

JM_MAIN_TIME_PATH = os.path.join(BASE_PATH, 'jm_main_time.txt')
MS_MAIN_TIME_PATH = os.path.join(BASE_PATH, 'ms_main_time.txt')
TIME_TIME_PATH = os.path.join(BASE_PATH, 'time_time.txt')
UPDATE_TIME_PATH = os.path.join(BASE_PATH, 'update_time.txt')
with open(JM_MAIN_TIME_PATH) as f:
    last_jm_main_updatetime = f.read()

with open(MS_MAIN_TIME_PATH) as f:
    last_ms_main_updatetime = f.read()

with open(TIME_TIME_PATH) as f:
    last_time_updatetime = f.read()

with open(UPDATE_TIME_PATH) as f:
    last_update_updatetime = f.read()

HUPDATETIME_DELTA_HOUR = -1
last_jm_main_updatetime = (datetime.strptime(last_jm_main_updatetime, "%Y-%m-%d %H:%M:%S") +
                   timedelta(hours=HUPDATETIME_DELTA_HOUR)).strftime('%Y-%m-%d %H:%M:%S')
last_ms_main_updatetime = (datetime.strptime(last_ms_main_updatetime, "%Y-%m-%d %H:%M:%S") +
                   timedelta(hours=HUPDATETIME_DELTA_HOUR)).strftime('%Y-%m-%d %H:%M:%S')
last_time_updatetime = (datetime.strptime(last_time_updatetime, "%Y-%m-%d %H:%M:%S") +
                   timedelta(hours=HUPDATETIME_DELTA_HOUR)).strftime('%Y-%m-%d %H:%M:%S')
last_update_updatetime = (datetime.strptime(last_update_updatetime, "%Y-%m-%d %H:%M:%S") +
                   timedelta(hours=HUPDATETIME_DELTA_HOUR)).strftime('%Y-%m-%d %H:%M:%S')

# 获取进门财经的数据
get_jinmen_data_sql = """
    select a.*, b.host, b.host_title, b.guest, b.guest_title,b.memo,b.if_important
    from app_research_service.JINMENCAIJING_MAIN a
    left join app_research_service.JINMENCAIJING_GUEST b on a._ID = b.ID
    where a.hupdatetime>'{last_updatetime}'
""".format(last_updatetime=last_jm_main_updatetime)

# 获取每市的数据
get_meishi_data_sql = """
    select a.*, b.host, b.host_title, b.guest, b.guest_title,b.memo,b.if_important
    from app_research_service.MEISHI_MAIN a
    left join app_research_service.MEISHI_GUEST b on a._ID = b.ID
    where a.hupdatetime>'{last_updatetime}'
""".format(last_updatetime=last_ms_main_updatetime)

# 内部路演主表
get_app_max_id_sql = """
    select max(roadshow_id) max_roadshow_id from app_research_service.ROADSHOW_MAIN where hisvalid =1
"""
# 已有路演原ID
get_app_id_sql = """
    select id from app_research_service.ROADSHOW_MAIN where hisvalid =1
"""
# 此次新增的数据中的历史数据
get_app_new_history_sql = """
    select id,roadshow_id,stime from app_research_service.ROADSHOW_MAIN where hisvalid =1 
"""

# 股票信息
get_stock_sql = """
    select sec_hcode,comb_symbol,exch_hcode from analytics_master_data.MDB_ENTITY_SECURITY
    where  exch_hcode in('SZ', 'SH', 'HK', 'BJ') and hisvalid=1 and sec_type='STK'
"""
# 行业信息
get_ind_sql = """
    select hcode ind_hcode,code sw_code,cname ind_name from analytics_master_data.MDB_ENTITY_INDUSTRY where src ='61b' and level='sw1' and hisvalid=1
"""
# 判断是否首次覆盖
all_data_sql = """
    select id,sec_json,sec_name,comp_hcode,stime from app_research_service.ROADSHOW_MAIN where sec_json 
    is not null
"""
insert_roadshow_main_sql = """
    INSERT INTO app_research_service.ROADSHOW_MAIN(id, stime, first_cover,first_cover_inst)
    VALUES (%s, %s, %s, %s) on duplicate
    key update id = values(id), stime = values(stime), 
    first_cover = values(first_cover), first_cover_inst = values(first_cover_inst)
"""
# 路演回放数据
get_jinmen_time_sql = """
    select a._ID,a.DT,a.PLAYCOUNT,a.BROWSECOUNT,a.DAILY_PLAYCOUNT_INCREASE,a.DAILY_BROWSECOUNT_INCREASE,a.heat,b.ROADSHOW_ID
    from app_research_service.JINMENCAIJING_TIME a
    left join app_research_service.ROADSHOW_MAIN b on a._id=b.id
    where a.hisvalid=1 and b.hisvalid=1 and a.hupdatetime>'{last_updatetime}'
""".format(last_updatetime=last_time_updatetime)
# 公司表
sql_insert_roadshow_main_sql = """
    INSERT INTO app_research_service.ROADSHOW_MAIN(id, roadshow_id, platform, stime, etime, duration, 
    appointments, title, if_important, sec_json, sec_name, sec_hcode, comb_symbol, industry_json, industry_name, 
    industry_hcode, authtag, `type`, content, uname, uid, occupation, company, comp_hcode, comp_cname, comp_csname, 
    sign, fanscount, subcount, guest, guest_title, host, host_title, memo, address, logo, avatarurl,create_by,update_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate
    key update id = values(id), roadshow_id = values(roadshow_id), platform = values(platform), stime = values(stime), 
    etime = values(etime), duration = values(duration), appointments = values(appointments), title = values(title), 
    if_important = values(if_important), sec_json = values(sec_json), sec_name = values(sec_name), 
    sec_hcode = values(sec_hcode), comb_symbol = values(comb_symbol), industry_json = values(industry_json), 
    industry_name = values(industry_name), industry_hcode = values(industry_hcode), authtag = values(authtag), 
    `type` = values(`type`), content = values(content), uname = values(uname), uid = values(uid), 
    occupation = values(occupation), company = values(company), comp_hcode = values(comp_hcode), 
    comp_cname = values(comp_cname), comp_csname = values(comp_csname), sign = values(sign), 
    fanscount = values(fanscount), subcount = values(subcount), guest = values(guest), guest_title = values(guest_title),
    host = values(host), host_title = values(host_title), memo = values(memo), address = values(address), 
    logo = values(logo), avatarurl = values(avatarurl), create_by = values(create_by), update_by = values(update_by)
"""
# 客户表
sql_insert_roadshow_client_sql = """
    INSERT INTO app_research_service.ROADSHOW_MAIN_CLIENT(id,roadshow_id,platform,stime,etime,duration,appointments,title,
    if_important,sec_json,comb_symbol,industry_json,industry_name,authtag,`type`,content,uname,uid,
    occupation,company,comp_cname,comp_csname,sign,fanscount,subcount,guest,guest_title,host,host_title,memo,address,
    logo,avatarurl,create_by,update_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate
    key update id = values(id), roadshow_id = values(roadshow_id), platform = values(platform), stime = values(stime), 
    etime = values(etime), duration = values(duration), appointments = values(appointments), title = values(title), 
    if_important = values(if_important), sec_json = values(sec_json), comb_symbol = values(comb_symbol), 
    industry_json = values(industry_json), 
    industry_name = values(industry_name), authtag = values(authtag), 
    `type` = values(`type`), content = values(content), uname = values(uname), uid = values(uid), 
    occupation = values(occupation), company = values(company),
    comp_cname = values(comp_cname), comp_csname = values(comp_csname), sign = values(sign), 
    fanscount = values(fanscount), subcount = values(subcount), guest = values(guest), guest_title = values(guest_title),
    host = values(host), host_title = values(host_title), memo = values(memo), address = values(address), 
    logo = values(logo), avatarurl = values(avatarurl), create_by = values(create_by), update_by = values(update_by)
"""

sql_insert_roadshow_playback_sql = """
    INSERT INTO app_research_service.ROADSHOW_PLAYBACK(id, roadshow_id, dt, playcount, browsecount, 
    daily_playcount_increase, daily_browsecount_increase, heat,create_by,update_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate
    key update id = values(id), roadshow_id = values(roadshow_id), dt = values(dt), playcount = values(playcount), 
    browsecount = values(browsecount), daily_playcount_increase = values(daily_playcount_increase), 
    daily_browsecount_increase = values(daily_browsecount_increase), heat = values(heat),create_by = values(create_by), update_by = values(update_by)
"""

