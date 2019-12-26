'''
    根据label分类文件
'''

from data_to_heavy import *

def classify_file_to_label(file_path):
    with open(file_path, 'r') as f:
        dict_info = json.loads(f.read())
        img_name = dict_info['imagePath']
        # for labels in dict_info['shapes']:
        try:
            if dict_info['scene'] in [0, 1]:
                return 0, img_name
            else:
                return 1, img_name
        except:
            print(file_path,'error--------')
            return 0,None


def create_dir(src):
    if not os.path.exists(src):
        os.makedirs(src)


if __name__ == '__main__':
    directory = '../wfk'
    new_dir_far = '../wfk/far_middle/'
    new_dir_near = '../wfk/near/'
    create_dir(new_dir_near)
    create_dir(new_dir_far)
    file_list = get_file(directory)
    for file_path in file_list:
        if os.path.splitext(file_path)[-1] == '.json':
            model,image_name = classify_file_to_label(file_path)
            if image_name:
                img_path = os.path.join(os.path.dirname(file_path), image_name)
                if model == '0':
                    new_dir = new_dir_far
                else:
                    new_dir = new_dir_near
                copy_file(file_path, new_dir)
                copy_file(img_path, new_dir)
                # print(file_path, '====>>命中')
