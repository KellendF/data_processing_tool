#统计每个json文件中的label，只要单label,然后把对应图片.jpg.json复制过去。
import os
import shutil
import json
import xml.etree.ElementTree as ET

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
            print(file_path)
            xml_path = os.path.join(src_dir,file_path)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            imagePath = root.find('filename').text
            imagePath = imagePath.split('/')[-1] # 有的filename标签值为图片路径需要处理
            labels = {}
            for object in root.findall('object'):
                label = object.find('name').text
                if label in damage_calsses_9:
                    if label in labels:  # python3的对应函数
                        n =labels[label]
                    else:
                        n = 0
                    labels[label] = 1 + n
                #print(len(labels),labels)
            if len(labels) == 1:
                for key in labels.keys():
                    if key in damage_calsses_9:
                        if not os.path.exists(dst_dir+'/'+key):
                            os.makedirs(dst_dir+'/'+key)
                        print(key,imagePath)
                        shutil.copy(os.path.join(src_dir, imagePath), dst_dir+'/'+key+'/'+imagePath)
                        shutil.copy(os.path.join(src_dir, file_path), dst_dir+'/'+key+'/'+file_path)

if __name__ == '__main__':
    src_dir = '../test/part_damage_jpg_xml/'
    dst_dir = '../test/damage9_part'
    classifier_label(src_dir,dst_dir)
