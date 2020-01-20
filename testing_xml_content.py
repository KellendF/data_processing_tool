'''

'''

import os
import shutil
from data_to_heavy import *
import xml.etree.ElementTree as ET
import time

def get_img_name(src):
    # try:
    tree = ET.parse(src)
    root = tree.getroot()
    imagePath = root.find('path').text
    print(imagePath)
    image_name = imagePath.split('/')[-1]
    print(image_name)
    root.find('filename').text = image_name
    labelinfo = root.find('labelInfo')
    labelinfo.find('title').text = image_name
    tree.write(src,encoding='utf-8')
    time.sleep(0.01)
    return image_name
    # except:
    #     move_file(src,'../test/error_file/')


if __name__ == '__main__':
    path = '../test/jpg_xml/'
    file_list = get_file(path)
    for file_path in file_list:
        if file_path.endswith('.xml'):
            img_name = get_img_name(file_path)
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