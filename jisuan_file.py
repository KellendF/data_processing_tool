'''
    计算文件数量
'''

from data_to_heavy import *


if __name__ == '__main__':
    path = '../data_1200'
    file_list = get_file(path)
    list = []
    for i in file_list:
        if os.path.splitext(i)[-1] in ['.jpeg', '.JPG', '.jpg', '.png']:
            list.append(i)

    # for i in file_list:
    #     type = os.path.splitext(i)[-1]
    #     list.append(type)
    # print(set(list))

    print(len(list))