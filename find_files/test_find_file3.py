'''
    提取部件中损伤（占比求法）
'''
from find_files.dir_tool import get_file
import json
import os
import re
import numpy as np
import shutil
# from find_files.judge import *
import cv2 as cv


damage_9 = ["boliposun","boliliewen","huahen","guaca","aoxian","zhezhou","silie","jichuan","queshi"]
# damage_9 = ['aoxian']

def find_damage(file_path,part):
    '''

    @param file_path: 文件路径
    @param part: 部件名称
    @return: 损伤点列表，部件点列表
    '''
    damage_point = []
    part_point = []
    img_size = None
    image_name = None
    with open(file_path,'r') as f:
        info = f.read()
        pattern = re.compile(part)
        if pattern.findall(info):
            info_dict = json.loads(info)
            image_name = info_dict['imagePath']
            image_height = info_dict['imgHeight']
            image_Width = info_dict['imgWidth']
            img_size = (int(image_height),int(image_Width))
            for labels in info_dict['shapes']:
                if labels['label'] in damage_9:
                   damage_point.append(labels['points'])
                if labels['label'] == part:
                    part_point = labels['points']
            return damage_point,part_point,image_name,img_size
    return damage_point,part_point,image_name,img_size



def judge_point(damage_point,part_point,img_size):
    '''
    判断损伤是否在部件上
    @param damage_point:损伤点列表
    @param part_point:部件点
    @return: True/False
    '''
    if not damage_point:
        return False
    img_arr = np.zeros(img_size,dtype = np.uint8)
    part_point_arr = np.array([part_point],dtype = np.int32)
    cv.fillPoly(img_arr, part_point_arr, 255)
    part_list = np.argwhere(img_arr == 255)
    part_tuple = tuple(map(tuple, part_list))
    for j,damage in enumerate(damage_point):
        damage_point_arr = np.array([damage],dtype = np.int32)
        cv.fillPoly(img_arr, damage_point_arr, j)
        damage_list = np.argwhere(img_arr == j)
        damage_tuple = tuple(map(tuple, damage_list))
        # r = [same_point for same_point in part_list if same_point in damage_list]
        r = set(part_tuple).intersection(set(damage_tuple))
        if len(r)/len(part_tuple) > 0.001:
            return True







if __name__ == '__main__':
    path = '../../test/QianBaoXianGangPi'
    part = 'QianBaoXianGangPi'
    out_dir = path+'/'+part+'/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    file_list = get_file(path)
    for file_path in file_list:
        if os.path.splitext(file_path)[1] == '.json':
            damage_point, part_point,image_name,img_size = find_damage(file_path,part)
            if image_name:
                if judge_point(damage_point, part_point,img_size):
                    img_path = os.path.join(os.path.dirname(file_path),image_name)
                    shutil.copy(file_path,out_dir)
                    shutil.copy(img_path,out_dir)
                    print(file_path,'--->命中')
    print('检测完成')






