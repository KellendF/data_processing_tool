#统计每个json文件中的label，只要单label,然后把对应图片.jpg.json复制过去。
import os
import shutil
import json

damage_calsses_9 = ["boliposun","boliliewen","huahen","guaca","aoxian","zhezhou","silie","jichuan","queshi"]
def classifier_label(src_dir,dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    if not os.path.exists(src_dir):
        print('目录不存在：' + src_dir)
    for root, dirs, files in os.walk(src_dir):
        for json_file in files:
            if not json_file.endswith('.json'):
                continue
            print(json_file)
            with open(os.path.join(src_dir, json_file), 'r') as load_f:
                labels=[]
                load_dict = json.load(load_f)
                shapes = load_dict['shapes']
                imagePath = load_dict['imagePath']
                labels = {}
                for i in range(0, len(shapes)):
                    label = shapes[i]['label']
                    points= shapes[i]['points']
                    #print(label,len(points))
                    # if len(points)==3:#找出无需标注的
                    #     shutil.move(os.path.join(image_dir, imagePath), dst_dir + '/' + imagePath)
                    #     shutil.move(os.path.join(src_dir, json_file), dst_dir+'/'+json_file)
                    # if cls.has_key(cls_name):#python2的函数
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
                            shutil.copy(os.path.join(src_dir, json_file), dst_dir+'/'+key+'/'+json_file)

if __name__ == '__main__':
    src_dir = '../test/jpg_json/'
    dst_dir = '../test/damage9'
    classifier_label(src_dir,dst_dir)
