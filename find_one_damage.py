'''
    查找只有一种损伤的文件
'''



from data_to_heavy import *



damage = {'guaca','aoxian'}
def find_one_damage_to_file(file_path):
    label_list = []
    with open(file_path,'r') as f:
        dict_info = json.loads(f.read())
        img_name = dict_info['imagePath']
        for labels in dict_info['shapes']:
            label_list.append(labels['label'])
    # if set(label_list) == damage or set(label_list) in damage:
    if set(label_list) == damage:
        return img_name







if __name__ == '__main__':
    directory = '../JY_data/segment/damage_9'
    new_dir = '../train/guaca/'
    file_list = get_file(directory)
    for file_path in file_list:
        if os.path.splitext(file_path)[-1] == '.json':
            image_name = find_one_damage_to_file(file_path)
            if image_name:
                img_path = os.path.join(os.path.dirname(file_path), image_name)
                copy_file(file_path,new_dir)
                copy_file(img_path,new_dir)
                print(file_path,'====>>命中')
