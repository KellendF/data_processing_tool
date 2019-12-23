'''
    计算文件数量
'''

from data_to_heavy import get_file


if __name__ == '__main__':
    path = '../JY_data/segment/glass/2019-12-13-singapore_glass_data'
    file_list = get_file(path)
    list = []
    for i in file_list:
        if i.endswith('.JPG'):
            list.append(i)
    print(len(list))