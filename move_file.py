'''
    移动目录下所有文件
'''
import os
import shutil
from multiprocessing import Process



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

def func(i,file_list):
    i += 1
    end_num = num * i
    if i == n:
        end_num = len(file_list)
    for j in range(num * (i - 1), end_num):
        move_file(file_list[j], new_dir.format(i))



def find_dir(path):
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

if __name__ == '__main__':
    path = '../zhousf/task_3'
    list_file = find_dir(path)
    new_dir = path+'/{}'
    n = 10
    num = len(list_file) // n
    if len(list_file) %n != 0:
         num += 1
    print(num)
    p_list = []
    for i in range(n):
        p = Process(target=func,args=(i,list_file))
        p.start()
    for j in p_list:
        j.join()

