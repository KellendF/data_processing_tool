
import os
import shutil
import json
import xml.etree.ElementTree as ET
from data_to_heavy import *

damage_calsses_9 = ["boliposun","boliliewen","huahen","guaca","aoxian","zhezhou","silie","jichuan","queshi"]
def classifier_label(src_dir,dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    if not os.path.exists(src_dir):
        print('目录不存在：' + src_dir)
    for root, dirs, files in os.walk(src_dir):
        for file_path in files:
            if not file_path.endswith('.xml'):
                continue
            xml_path = os.path.join(src_dir,file_path)
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                imagePath = root.find('filename').text
                imagePath = imagePath.split('/')[-1]
                for object in root.findall('object'):
                    label = object.find('name').text
                    if label not in damage_calsses_9:
                        img_path = os.path.join(src_dir,imagePath)
                        if  os.path.exists(img_path):
                            move_file(xml_path,dst_dir)
                            move_file(img_path,dst_dir)
                        else:
                            move_file(xml_path,'../test/error/')
            except:
                move_file(xml_path,'../test/error/')
if __name__ == '__main__':
    src_dir = '../test/damage/'
    dst_dir = '../test/part_damage/'
    classifier_label(src_dir,dst_dir)
