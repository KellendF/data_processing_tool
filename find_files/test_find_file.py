'''
    提取部件中损伤
'''
from data_to_heavy import get_file
import json
import os
import re
import shutil
from find_files.panduan import *
from find_files.judge import *

damage_9 = ["boliposun","boliliewen","huahen","guaca","aoxian","zhezhou","silie","jichuan","queshi"]

def find_damage(file_path,part):
    '''

    @param file_path: 文件路径
    @param part: 部件名称
    @return: 损伤点列表，部件点列表
    '''
    damage_point = []
    part_point = []
    image_name = None
    with open(file_path,'r') as f:
        info = f.read()
        pattern = re.compile(part)
        if pattern.findall(info):
            info_dict = json.loads(info)
            image_name = info_dict['imagePath']
            for labels in info_dict['shapes']:
                if labels['label'] in damage_9:
                   damage_point.append(labels['points'])
                if labels['label'] == part:
                    part_point = labels['points']
            return damage_point,part_point,image_name
    return damage_point,part_point,image_name

def judge_point(damage_point,part_point):
    '''
    判断损伤是否在部件上
    @param damage_point:损伤点列表
    @param part_point:部件点
    @return: True/False
    '''
    if not damage_point:
        return False
    for points in damage_point:
        for point in points:
            if point in part_point:
                continue
            # 判断改点与多边形的边相交次数
            times = isPointinPolygon(point,part_point)
            # 次数为奇数时表示点在多边形内
            if times % 2 != 0:
                return True
    for points in damage_point:
        for point in part_point:
            if point in points:
                continue
            times = isPointinPolygon(point,points)
            if times % 2 != 0:
                return True



def isPointinPolygon(point_1, point_2):
    '''
    判断某个点与多边形的边相交次数
    @param point_1: 单个点
    @param point_2: 多边形点列表
    @return:
    '''
    point_2.append(point_2[0])
    j = 0
    for i in range(len(point_2) - 1):
        # s = SegmentsIntersect(part_point[i],part_point[i+1],point,[0,0])
        # if s.result:
        #     j += 1
        # 输入直线两个端点和需要判断点的坐标
        s = Point(point_2[i], point_2[i + 1], point_1)
        # 判断点与[0,0]点组成的直线与输入直线是否相交
        if s.intersect():
            j += 1

        # a = np.array(part_point[i])
        # b = np.array(part_point[i+1])
        # c = a-b
        # d = np.array(point)
        # n = c[0]*d[1] - c[1]*d[0]
        # if n == 0 :
        #     continue
    #     j += 1

    return j





if __name__ == '__main__':
    path = '../train'
    part = 'QianBaoXianGangPi'
    out_dir = path+'/'+part+'/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    file_list = get_file(path)
    for file_path in file_list:
        if os.path.splitext(file_path)[1] == '.json':
            damage_point, part_point,image_name = find_damage(file_path,part)
            if image_name:
                if judge_point(damage_point, part_point):
                    img_path = os.path.join(os.path.dirname(file_path),image_name)
                    shutil.move(file_path,out_dir)
                    shutil.move(img_path,out_dir)
                    print(file_path,'--->命中')
    print('检测完成')






