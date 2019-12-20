'''
    数据处理工具
'''
import hashlib
import os,sys
import shutil
import json
import zipfile,tarfile


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


def get_file_info(file_path):
    '''
    校验文件计算md5值
    @param file_path: 文件完整路径
    @return: 该文件的md5值
    '''
    md5 = hashlib.md5()
    with open(file_path,'rb') as f:
        while True:
            fd = f.read(1024)
            if not fd:
                break
            md5.update(fd)
    return md5.hexdigest()


def unzip_file(zip_src):
    '''
    解压目录下的‘压缩’文件
    @param zip_src: 完整路径(传入文件时指定文件类型)
    @return: None
    '''
    if zip_src.endswith('.zip'):
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
    elif zip_src.endswith('.tar.gz'):
        dst_dir = zip_src.replace('.tar.gz', '')
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        try:
            print(dst_dir)
            t = tarfile.open(zip_src)
            t.extractall(path=dst_dir)
        except Exception as e:
            print(zip_src)
        remove_file(zip_src)




def rename_file(path,newname):
    '''
    更改文件名称
    @param path: 文件完整路径,文件新名称
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



def move_dir(path,new_dir):
    '''
    移动目录--复制当前目录下所有文件
    @param path:原路径
    @param new_dir: 新路径
    @return: None
    '''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    for mainpath, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(mainpath,file)
            dir_name = mainpath.split('/')[-1]
            new_dir_path = new_dir+'/'+dir_name+'/'
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
            new_file_path = os.path.join(new_dir_path,file)
            shutil.copyfile(file_path,new_file_path)


def move_file(old_path,new_dir):
    '''
    移动文件
    @param old_path:文件当前路径
    @param new_dir: 新目录
    @return: None
    '''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = new_dir+old_path.split('/')[-1]

    try:
        shutil.move(old_path,new_path)
    except:
        print('{} is error'.format(old_path))



def copy_file(old_path,new_dir):
    '''
    复制文件
    @param old_path:文件当前路径
    @param new_dir: 新目录
    @return: None
    '''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = new_dir+old_path.split('/')[-1]
    try:
        shutil.copyfile(old_path,new_path)
    except:
        print('{} is error'.format(old_path))



if __name__ == '__main__':
    has_list = []
    same_list = []
    EXT = ['.jpg','.png','.jpeg']
    i = 0
    path = '../filezilla_'
    file_list = get_file(path)
    for file_path in file_list:
        if os.path.splitext(file_path)[-1] in EXT:
            has = get_file_info(file_path)
            if has in has_list:
                i+= 1
                # shutil.move(file_path,'../train')
                same_list.append(file_path)
                continue
            has_list.append(has)

    print(same_list)
    print('有{}个相同文件'.format(i))

    #
    # with open('../test/yunce_aoxian_000001_022_055.jpg','rb') as f:
    #     data = f.read()
    #     print(hashlib.md5(data).hexdigest())