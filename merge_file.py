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
    file_list1 = get_file('../filezilla_/part/part_data_new/part_data_new')
    file_list2 = get_file('../filezilla_/part/part_data_new/part_jpg_new')
    for file in file_list1:
        if file.endswith('.json'):
            copy_file(file,'../filezilla_/part/part_data_new/part_data/')

    for file in file_list2:
        copy_file(file,'../filezilla_/part/part_data_new/part_data/')