'''
    合并文件
'''

import shutil
from find_files.dir_tool import *

def move_file(old_path,new_dir):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = new_dir+old_path.split('/')[-1]

    try:
        shutil.move(old_path,new_path)
    except:
        print('{} is error'.format(old_path))



def copy_file(old_path,new_dir):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = new_dir+old_path.split('/')[-1]
    try:
        shutil.copyfile(old_path,new_path)
    except:
        print('{} is error'.format(old_path))


if __name__ == '__main__':
    file_list1 = get_file('../test')
    for file in file_list1:
        # move_file(file, '../test/jpg_json/')
        if os.path.splitext(file)[-1] in ['.jpeg', '.JPG', '.jpg', '.png','.PNG']:
        # if
            move_file(file, '../test/1/')
        elif os.path.splitext(file)[-1] in ['.zip','.rar']:
            move_file(file,'../test/2/')
        # else:
        #     move_file(file,'../test/file/')
        # if file.endswith('.xml'):
        #     move_file(file,'../test/20190411-whole-yunju-jpg/')
    print('移动完成')
