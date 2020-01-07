

'''

'''
import hashlib
import os
import shutil
from data_to_heavy import *
import filetype

class Move_file(object):

    def __init__(self,path):
        self.path = path
        self.img_info_list = []
        self.tar_info_list = []
        self.other_info_list = []
        self.tar_num = 0
        self.img_num = 0
        self.other_num = 0
        self.same_tar_num = 0
        self.same_img_num = 0
        self.same_other_num = 0

    def get_file_info(self,file_path):
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

    def move_file(self,old_path,new_dir):
        '''
        移动并合并文件
        @param old_path:
        @param new_dir:
        @return:
        '''
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_path = new_dir+old_path.split('/')[-1]

        try:
            shutil.move(old_path,new_path)
        except:
            print('{} is error'.format(old_path))

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

    def run(self):
        file_list = get_file(self.path)
        self.file_num = len(file_list)
        for file_path in file_list:
            # if os.path.splitext(file_path)[-1] in ['.jpeg', '.JPG', '.jpg', '.png', '.PNG']:
            try:
                file_type = filetype.guess(file_path).extension
            except Exception as e:
                file_type = None
            if file_type in ['jpg','png']:
                img_md5 = self.get_file_info(file_path)
                new_img_path = self.rename_file(file_path,img_md5)
                if img_md5 in self.img_info_list:
                    self.move_file(new_img_path,'../test/same_img/')
                    self.same_img_num += 1
                    continue
                self.img_info_list.append(img_md5)
                # 移动更改名称后的图片到
                self.move_file(new_img_path,'../test/img/')
                self.img_num += 1
            elif file_type in ['zip','rar']:
                tar_md5 = self.get_file_info(file_path)
                new_tar_path = self.rename_file(file_path, tar_md5)
                if tar_md5 in self.tar_info_list:
                    self.move_file(new_tar_path, '../test/same_tar/')
                    self.same_tar_num += 1
                    continue
                self.tar_info_list.append(tar_md5)
                # 移动更改名称后的待解压文件
                self.move_file(new_tar_path, '../test/tar/')
                self.tar_num += 1
            else:
                other_md5 = self.get_file_info(file_path)
                new_other_path = self.rename_file(file_path, other_md5)
                if other_md5 in self.other_info_list:
                    self.move_file(new_other_path, '../test/same_other/')
                    self.same_other_num += 1
                    continue
                self.other_info_list.append(other_md5)
                self.move_file(new_other_path,'../test/other_file/')
                self.other_num += 1

        final = '总共{}文件，图片移动成功{}张，相同图片{}，代解压文件{}个，相同解压文件{}，其他文件{}，相同其他文件{}'.format(self.file_num,self.img_num,self.same_img_num,self.tar_num,self.same_tar_num,self.other_num,self.same_other_num)
        with open('final.txt','w') as f:
            f.write(final)
        print(final)



if __name__ == '__main__':
    path = '../test/'
    p = Move_file(path)
    p.run()

