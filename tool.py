'''
    处理重复文件小工具
'''
import hashlib
import os

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
    file_type = path.split('.')[-1]
    name = newname + '.' + file_type
    oldname = path.split('/')[-1]
    newpath = path.replace(oldname,name,1)
    os.rename(path,newpath)

def remove_file(path):
    '''
    删除文件
    @param path: 文件完整路径
    @return: None
    '''
    if os.path.exists(path):
        os.remove(path)


if __name__ == '__main__':
    img_set = []
    path = '../u=3437217665,1564280326&fm=26&gp=0.jpg'
    filename = get_filename(path)
    


