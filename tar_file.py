'''
    解压文件
'''
import zipfile,tarfile
import os
from tool import remove_file
from data_to_heavy import get_file
import rarfile
import filetype
import shutil


def move_file(old_path, new_dir):
    '''
    移动并合并文件
    @param old_path:
    @param new_dir:
    @return:
    '''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = new_dir + old_path.split('/')[-1]

    try:
        shutil.move(old_path, new_path)
    except:
        print('{} is error'.format(old_path))

def unzip_file(zip_src):
    '''
    解压目录下的‘压缩’文件
    @param zip_src: 完整路径(传入文件时指定文件类型)
    @return: None
    '''
    try:
        file_type = filetype.guess(zip_src).extension
    except Exception as e:
        file_type = None
    if file_type == 'zip':
        r = zipfile.is_zipfile(zip_src)
        dst_dir = zip_src.replace('.zip','')
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        if r:
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in fz.namelist():
                try:
                    fz.extract(file, dst_dir)
                except:
                    print(file)
                remove_file(zip_src)

    elif  file_type == 'gz':
        dst_dir = zip_src.replace('.tar.gz', '')
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        try:
            t = tarfile.open(zip_src)
            t.extractall(path=dst_dir)
        except Exception as e:
            print(zip_src)
        remove_file(zip_src)
    elif file_type == 'rar':
        dst_dir = zip_src.replace('.rar', '')
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        try:
            rf = rarfile.RarFile(zip_src)
            rf.extractall(os.path.dirname(zip_src))
        except Exception as e:
            print(zip_src)
        remove_file(zip_src)
    else:
        directory = os.path.dirname(zip_src)+'error'
        move_file(zip_src,directory)




if __name__ == '__main__':
    EXT = ['.gz','.zip','.rar']
    path = '../test/score/'
    file_list = get_file(path)
    for file in file_list:
        unzip_file(file)
        # print(os.path.splitext(file))
        # if os.path.splitext(file)[-1] in EXT:
        #     unzip_file(file)
    print('执行成功')