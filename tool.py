'''
    处理重复文件小工具
'''
import hashlib
import os
import filetype

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

if __name__ == '__main__':
    path = '../train/123/123.JPG'
    # print(judge_filetype(path))
    rename_file(path,'456')


