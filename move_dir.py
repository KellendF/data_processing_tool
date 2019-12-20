'''
    移动目录下所有文件
'''
import os
import shutil
from multiprocessing import Process


def move_dir(path,new_dir):
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

def func(i,list_dir):
    i += 1
    end_num = num * i
    if i == n:
        end_num = len(list_dir)
    for j in range(num * (i - 1), end_num):
        move_dir(list_dir[j], new_dir.format(i))


def find_dir(path):
    dir_list = []
    files = os.listdir(path)
    for file_name in files:
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            dir_list.append(file_path)
    return dir_list

if __name__ == '__main__':
    path = '../train/data'
    list_dir = find_dir(path)
    new_dir = '../train/task_{}'
    n = 3
    num = len(list_dir) // n
    print(num)
    # for i in range(n):
    #     i+=1
    #     end_num = num*i
    #     if i == n:
    #        end_num = len(list_dir)
    #     for j in range(dir_num,end_num):
    #         move_dir(list_dir[j], new_dir.format(i))
    #     dir_num = num*i
    p_list = []
    for i in range(n):
        p = Process(target=func,args=(i,list_dir))
        p.start()
    for j in p_list:
        j.join()

