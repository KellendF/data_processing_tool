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
          'describe varchar(200),' \
          'company varchar(20),' \
          'file_type char(4),' \
           'width int,'\
          'height int);'
    sql2 = 'create table damage(' \
          'name char(32)  primary key,' \
          'source varchar(100),' \
          'describe varchar(200),' \
          'company varchar(20),'\
          'file_type char(4),' \
           'data_type char(4),' \
           'width int,' \
           'height int);'
    cur.execute(sql1)
    cur.execute(sql2)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_db()

