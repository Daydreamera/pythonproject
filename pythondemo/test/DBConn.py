
import pymysql
import cx_Oracle
import pandas as pd
# ��oracle���ó�����
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class DBConn(object):
    def __init__(
            self,
            dbtype='', host='', port='', user='', passwd='', dbname=''
    ):
        self.dbtype = dbtype
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        if dbtype == 'mysql':
            self.db = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd,
                                      db=self.dbname, charset='utf8mb4')
        elif dbtype == 'oracle':
            self.db = cx_Oracle.connect(self.user, self.passwd, self.host + ':' + self.port + '/' + self.dbname)

    # ����sql
    def bulk_insert_mysql(self, sql, record_list):
        cursor = self.db.cursor()
        cursor.executemany(sql, record_list)
        self.db.commit()
        cursor.close()

    def get_sql(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_sql_result_pd(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        # ��ȡ���Ӷ����������Ϣ
        columnDes = cursor.description
        columnNames = [columnDes[i][0].lower() for i in range(len(columnDes))]
        df = pd.DataFrame(data, columns=columnNames)
        return df

    def update_sql(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()