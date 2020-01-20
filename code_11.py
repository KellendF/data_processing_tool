#统计每个json文件中的label，只要单label,然后把对应图片.jpg.json复制过去。
import os
import shutil
import json

damage_calsses_9 = ["boliposun","boliliewen","huahen","guaca","aoxian","zhezhou","silie","jichuan","queshi"]
damage = ["zhezhou","aoxian"]
damage_zhezhou = ['zhezhou']
def classifier_label(src_dir,dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    if not os.path.exists(src_dir):
        print('目录不存在：' + src_dir)
    for root, dirs, files in os.walk(src_dir):
        for json_file in files:
            if not json_file.endswith('.json'):
                continue
            with open(os.path.join(src_dir, json_file), 'r') as load_f:
                labels=[]
                load_dict = json.load(load_f)
                shapes = load_dict['shapes']
                imagePath = load_dict['imagePath']
                # labels = {}
                for i in range(0, len(shapes)):
                    label = shapes[i]['label']
                    if label in damage_calsses_9:
                        labels.append(label)
                if set(labels) == set(damage):
                    shutil.copy(os.path.join(src_dir, imagePath), dst_dir + imagePath)
                    shutil.copy(os.path.join(src_dir, json_file), dst_dir + json_file)
                elif set(labels) == set(damage_zhezhou):
                    shutil.copy(os.path.join(src_dir, imagePath), dst_dir + imagePath)
                    shutil.copy(os.path.join(src_dir, json_file), dst_dir + json_file)

if __name__ == '__main__':
    src_dir = '../test/jpg_json/'
    dst_dir = '../test/damage/'
    classifier_label(src_dir,dst_dir)
    # print(damage_zhezhou == ['zhezhou'])

