'''
    获取当前目录下所有文件
'''
import os
import json
from multiprocessing import Process
import xml.etree.ElementTree as ET

def get_file(path):
    """
    获取当前目录下所有文件
    @param path: 主目录完整路径
    @return: 当前目录下的所有文件列表
    """
    file_list = []
    for path, _, files in os.walk(path):
        if files:
            for filename in files:
                file_list.append(os.path.join(path, filename))
    return file_list

# def func(xml_path):
#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#     imagePath = root.find('filename').text
#     labels = {}
#     for object in root.findall('object'):
#         label = object.find('name').text
#         if label in labels:  # python3的对应函数
#             n = labels[label]
#         else:
#             n = 0
#         labels[label] = 1 + n




if __name__ == '__main__':
    label_dict = {}
    file_list = get_file('../train/')
    print(len(file_list))
    for file in file_list:
        if file.endswith('.xml'):
            tree = ET.parse(file)
            root = tree.getroot()
            imagePath = root.find('filename').text
            for object in root.findall('object'):
                label = object.find('name').text
                if label in label_dict:  # python3的对应函数
                    n = label_dict[label]
                else:
                    n = 0
                label_dict[label] = 1 + n
    with open('../statistic.json', 'w') as f:
        label_dict = json.dumps(label_dict)
        f.write(label_dict)

    print(label_dict)




