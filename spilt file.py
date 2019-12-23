'''
    拆分文件
'''
from data_to_heavy import *

def split_file(path):
    '''
    将文件夹下相同名称的不同文件类型拆分到不同文件夹下
    @param path:
    @return:
    '''
    if os.path.splitext(path)[-1] == '.json':
        create_dir_move_file(path,'json')
    if os.path.splitext(path)[-1] in ['.jpg','.JPG','.png']:
        create_dir_move_file(path,'jpg')
    if os.path.splitext(path)[-1] == '.xml':
        create_dir_move_file(path,'xml')




def create_dir_move_file(path,model):
    dir_path = os.path.dirname(path)
    dir_name = dir_path.split('/')[-1].replace('data',model)
    directory = os.path.join(dir_path,dir_name)
    print(directory)
    new_path = os.path.join(directory,path.split('/')[-1])
    print(new_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        shutil.move(path, new_path)
    except:
        print('{} is error'.format(path))


if __name__ == '__main__':
    path = '../JY_data/segment/glass/2019-12-13-singapore_glass_data'
    file_list = get_file(path)
    for file_path in file_list:
        split_file(file_path)
    print('移动完成')