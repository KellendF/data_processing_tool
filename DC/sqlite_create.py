'''
    sqlite表创建
'''
import sqlite3

def create_db():
    '''

    @return:
    '''
    conn = sqlite3.connect('data.db')
    cur =conn.cursor()
    sql1 = 'create table part(' \
          'name char(32) primary key,' \
          'source varchar(100),' \
          'data_type char(10),' \
          'company varchar(50),' \
          'file_type char(10),' \
           'width int,'\
          'height int);'
    sql2 = 'create table damage(' \
          'name char(32)  primary key,' \
          'source varchar(100),' \
          'data_type char(10),' \
          'company varchar(50),'\
          'file_type char(10),' \
           'describe varchar(100),' \
           'width int,' \
           'height int,' \
           'guaca int,' \
           'aoxian int,' \
           'huahen int,' \
           'boliposun int,' \
           'boliliewen int,' \
           'zhezhou int,' \
           'silie int,' \
           'jichuan int,' \
           'queshi int);'
    cur.execute(sql1)
    cur.execute(sql2)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_db()

