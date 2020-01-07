'''
    移动目录下所有文件
'''
import os
import shutil
from multiprocessing import Process


def move_dir(path,new_dir):
    '''
    根据文件夹分
    @param path:
    @param new_dir:
    @return:
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
            shutil.move(file_path,new_file_path)


def func(i,file_list):
    i += 1
    end_num = num * i
    if i == n:
        end_num = len(file_list)
    for j in range(num * (i - 1), end_num):
        move_dir(file_list[j], new_dir.format(i))


def find_dir(path):
    '''
    获取当前文件夹下所有目录
    @param path:
    @return:
    '''
    dir_list = []
    files = os.listdir(path)
    for file_name in files:
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            dir_list.append(file_path)
    return dir_list



if __name__ == '__main__':
    path = '../zhousf/task_3'
    list_file = find_dir(path)
    new_dir = path+'/{}'
    n = 10
    num = len(list_file) // n
    print(num)
    p_list = []
    for i in range(n):
        p = Process(target=func,args=(i,list_file))
        p.start()
    for j in p_list:
        j.join()

