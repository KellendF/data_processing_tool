'''
    检测json文件中图片名称是否更改，判断json文件是否可以完整打开，判断图片名称是否为hash值
'''

import os
import shutil
from data_to_heavy import *


def get_img_name(src):
    try:
        with open(src,'r') as f:
            info = f.read()
            info_dict = json.loads(info)
            image_name = info_dict['imagePath']
            return image_name
    except:
        move_file(src,'../test/error_file/')


if __name__ == '__main__':
    path = '../test/jpg_json/'
    file_list = get_file(path)
    for file_path in file_list:
        if file_path.endswith('.json'):
            img_name = get_img_name(file_path)
            print(img_name)
            if img_name:
                img_path = os.path.join(path,img_name)
                if not os.path.exists(os.path.join(path,img_name)):
                    move_file(file_path,'../test/error_name_file/')
                else:
                    imd5 = get_file_info(img_path)
                    if imd5 == img_name.split('.')[0]:
                        continue
                    else:
                        move_file(file_path,'../test/rename/')
                        move_file(img_path,'../test/rename/')