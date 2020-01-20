'''
    数据清洗
    将目录下所有图片进行查重，重名名为该图片的md5值，将该图片的md5值与数据库中的name字段进行比较，存在部件移动到part文件夹，损伤相同，
'''
import os
import sqlite3
import hashlib
import json
import shutil
import time

class JudgeDb(object):
    def __init__(self,path):
        self.path = path
        self.img_info = []
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        self.part_num = 0
        self.damage_num = 0
        self.del_num = 0

    def get_file(self, path):
        """
        获取当前目录下所有文件
        @param path: 主目录完整路径
        @return: 当前目录下的所有文件列表
        """
        file_list = []
        for path, _, files in os.walk(path):
            if files:
                for filename in files:
                    file_list.append(os.path.join(path, filename))
        return file_list

    def get_file_info(self, file_path):
        '''
        校验文件计算md5值
        @param file_path: 文件完整路径
        @return: 该文件的md5值
        '''
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                fd = f.read(1024)
                if not fd:
                    break
                md5.update(fd)
        return md5.hexdigest()

    def judge_file_to_db(self, table, value):
        '''
        判断数据库中是否有相同数据
        @param value: 图片md5值
        @param type: 上传的类型（‘部件’，‘损伤’）
        @return: 存在返回True,不存在返回False
        '''
        sql = 'select * from %s where name = "%s";' % (table, value)
        self.cur.execute(sql)
        if self.cur.fetchone():
            return True
        return False

    def rename_file(self, path, newname):
        '''
        更改文件名称
        @param path: 文件完整路径,文件新名称
        @return: None
        '''
        oldname = path.split('/')[-1].split('.')[0][::-1]
        newpath = path[::-1].replace(oldname, newname[::-1], 1)[::-1]
        try:
            os.rename(path, newpath)
        except Exception as e:
            print(e)
        return newpath

    def move_file(self, old_path, new_dir):
        '''
        移动文件
        @param old_path:文件当前路径
        @param new_dir: 新目录
        @return: None
        '''
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_path = new_dir + old_path.split('/')[-1]
        try:
            shutil.move(old_path, new_path)
        except:
            print('{} is error'.format(old_path))

    def copy_file(self, old_path, new_dir):
        '''
        复制文件
        @param old_path:文件当前路径
        @param new_dir: 新目录
        @return: None
        '''
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_path = new_dir + old_path.split('/')[-1]
        try:
            shutil.copyfile(old_path, new_path)
        except:
            print('{} is error'.format(old_path))

    def run(self):
        file_list = self.get_file(self.path)
        self.sum_num = len(file_list)
        for file_path in file_list:
            if not os.path.exists(file_path):
                continue
            img_md5 = self.get_file_info(file_path)
            new_path = self.rename_file(file_path, img_md5)
            if img_md5 in self.img_info:
                self.del_num += 1
                continue
            self.img_info.append(img_md5)
            if self.judge_file_to_db('part',img_md5):
                self.move_file(new_path,'../../test/part/')
                self.part_num += 1
            if self.judge_file_to_db('damage',img_md5):
                if os.path.exists(new_path):
                    self.move_file(new_path, '../../test/damage/')
                    self.damage_num += 1
                else:
                    part_path = '../../test/part/'+ new_path.split('/')[-1]
                    self.copy_file(part_path,'../../test/damage/')
                    self.damage_num += 1
            print(img_md5,'=======process ok')
        print('处理完成删除数量{}，与部件相同{}，与损伤相同{}'.format(self.del_num,self.part_num,self.damage_num))


if __name__ == '__main__':
    path = '../../test/img/'
    d = JudgeDb(path)
    start = time.time()
    d.run()
    end = time.time()
    print('共用时%s'%(end-start))