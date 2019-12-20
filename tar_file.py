'''
    解压文件
'''
import zipfile,tarfile
import os
from tool import remove_file
from data_to_heavy import get_file


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
            t = tarfile.open(zip_src)
            t.extractall(path=dst_dir)
        except Exception as e:
            print(zip_src)
        remove_file(zip_src)



if __name__ == '__main__':
    EXT = ['.gz','.zip']
    path = '../filezilla_/damage_9'
    file_list = get_file(path)
    for file in file_list:
        print(os.path.splitext(file))
        if os.path.splitext(file)[-1] in EXT:
            unzip_file(file)
    print('执行成功')