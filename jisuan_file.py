'''
    计算文件数量
'''

from data_to_heavy import *


if __name__ == '__main__':
    path = '../test/damage3_jpg_json_2/'
    file_list = get_file(path)
    print(len(file_list))
    list = []
    for i in file_list:
        # list.append(i)
        if os.path.splitext(i)[-1] in ['.jpeg', '.JPG', '.jpg', '.png','.PNG']:

            list.append(i)
        # else:
        #     print(i)
    # for i in file_list:
    #     type = os.path.splitext(i)[-1]
    #     list.append(type)
    # print(set(list))

    print(len(list))