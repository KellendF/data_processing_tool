'''
    获取当前目录下所有文件
'''
import os
import json
from multiprocessing import Process

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

# def func():
#     while file_list:
#         file = file_list.pop()
#         if file.endswith('.json'):
#             with open(file, 'r') as f:
#                 json_info = f.read()
#                 dict_info = json.loads(json_info)
#                 for label_ in dict_info['shapes']:
#                     label = label_['label']
#                     if label in label_dict.keys():
#                         label_dict[label] += 1
#                     else:
#                         label_dict[label] = 1




if __name__ == '__main__':
    label_dict = {}
    file_list = get_file('../../train')
    print(len(file_list))
    # q = []
    # for i in range(5):
    #     p = Process(target=func)
    #     q.append(p)
    #     p.start()
    # for i in q:
    #     i.join()


    for file in file_list:
        if file.endswith('.json'):
            with open(file,'r') as f:
                json_info = f.read()
                dict_info = json.loads(json_info)
                for label_ in dict_info['shapes']:
                    label = label_['label']
                    if label in label_dict.keys():
                        label_dict[label] += 1
                    else:
                        label_dict[label] = 1
    with open('../statistic.json', 'w') as f:
        label_dict = json.dumps(label_dict)
        f.write(label_dict)

    print(label_dict)




