'''
    计算文件数量
'''

from data_to_heavy import get_file


if __name__ == '__main__':
    path = '../JY_data/RenBao_huan_xiu/RenBao_huan_xiu_20190708'
    file_list = get_file(path)
    print(len(file_list))