'''

'''
import numpy as np
import json
import mahotas.polygon
import cv2 as cv

# img_size = (10,10)
# part_point = [[1,1],[3,1],[6,3],[7,3],[7,6],[8,2],[9,1]]
# damage_point = [[4,1],[4,6],[3,8],[5,8],[2,6]]
#
# img_arr = np.zeros(img_size)
# part_point_tuple = [tuple(point) for point in part_point]
# mahotas.polygon.fill_polygon(part_point_tuple, img_arr, color=1)
# list = np.argwhere(img_arr==1)
# print(list)
# for damage in damage_point:
#     mahotas.polygon.fill_polygon(damage, img_arr, color=2)
# damage_point_tuple = [tuple(point) for point in damage_point]
# mahotas.polygon.fill_polygon(damage_point_tuple, img_arr, color=2)

# print(img_arr)

if __name__ == '__main__':
    damage_9 = ["boliposun", "boliliewen", "huahen", "guaca", "aoxian", "zhezhou", "silie", "jichuan", "queshi"]
    path = '../../train/259944-IMG_9419.json'
    with open(path,'r') as f:
        info = f.read()
        damage_point = []
        info_dict = json.loads(info)
        # image_name = info_dict['imagePath']
        image_height = info_dict['imgHeight']
        image_Width = info_dict['imgWidth']
        img_size = (int(image_height), int(image_Width))

        for labels in info_dict['shapes']:
            if labels['label'] == 'QianBaoXianGangPi':
                part_point = labels['points']
            if labels['label'] in damage_9:
                print(labels['label'])
                damage_point.append(labels['points'])
        img_arr = np.zeros(img_size, dtype=np.uint8)
        part_point_arr = np.array([part_point], dtype=np.int32)
        cv.fillPoly(img_arr, part_point_arr, 255)
        image, contours, hierarchy = cv.findContours(img_arr, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # cv.drawContours(img_arr,contours,-1,0,1)
        cv.drawContours(img_arr,part_point_arr,-1,125,3)
        part_list = np.argwhere(img_arr == 255)
        part_list = tuple(map(tuple, part_list))

        cv.imshow('ll',img_arr)
        for j, damage in enumerate(damage_point):
            j+=1
            damage_point_arr = np.array([damage], dtype=np.int32)
            cv.fillPoly(img_arr, damage_point_arr, j*20)
            damage_list = np.argwhere(img_arr == j*20)
            damage_list = tuple(map(tuple, damage_list))
            r = set(part_list).intersection(set(damage_list))
            print(len(r))
            print(len(part_list),'-->',len(damage_list))

        cv.imshow('qian',img_arr)
        cv.waitKey()