'''
    处理重复文件小工具
'''
import hashlib
import os
import filetype
import shutil

def get_filename(path):
    """
    获得文件hash值
    @param path: '/home/ubuntu/'
    @return : 返回文件的hash值作为文件名称
    """
    with open(path,'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()


def rename_file(path,newname):
    '''
    更改文件名称
    @param path: 文件完整路径
    @return: None
    '''
    oldname = path.split('/')[-1].split('.')[0][::-1]
    print(oldname)
    newpath = path[::-1].replace(oldname,newname[::-1],1)[::-1]
    print(newpath)
    os.rename(path,newpath)

def remove_file(path):
    '''
    删除文件
    @param path: 文件完整路径
    @return: None
    '''
    if os.path.exists(path):
        os.remove(path)


def judge_filetype(path):
    return filetype.guess(path).extension

def get_file(path):
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

def move_file(file_path,new_dir):
    '''
    根据文件分
    @param file_path:
    @param new_dir:
    @return:
    '''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    # new_file_path = os.path.join(new_dir_path, file)
    shutil.move(file_path, new_dir)


if __name__ == '__main__':
    list = []
    path1 = '../test/middle_near_data/bujian_jpg_json/'
    path2 = '../test/img/'
    for src in os.listdir(path2):
        list.append(get_filename(os.path.join(path2,src)))
    file_list = get_file(path1)
    for file_path in file_list:
        if file_path.split('/')[-1].split('.')[0] in list:
            move_file(file_path,'../test/images/')
        # if file_path.split('.jpg'):
        #     print(file_path,get_filename(file_path))

    # print(judge_filetype(path))
    # rename_file(path,'456')
    # remove_file(path)


