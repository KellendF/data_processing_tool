'''

'''

import xmltodict
import json
import os


# json to xml
def jsonToXml(json_str):
    try:
        xml_str = ""
        xml_str = xmltodict.unparse(json_str, encoding='utf-8')
    except:
        xml_str = xmltodict.unparse({'request': json_str}, encoding='utf-8')
    finally:
        return xml_str


def json_to_xml(json_path, xml_path):
    if (os.path.exists(xml_path) == False):
        os.makedirs(xml_path)
    dir = os.listdir(json_path)
    for file in dir:
        file_list = file.split(".")
        with open(os.path.join(json_path, file), 'r') as load_f:
            load_dict = json.load(load_f)
        json_result = jsonToXml(load_dict)
        f = open(os.path.join(xml_path, file_list[0] + ".xml"), 'w', encoding="UTF-8")
        f.write(json_result)
        f.close()


if __name__ == '__main__':
    json_path = r"/home/zhang/下载/SEG_task/Annotation/O_11_json"  # 该目录为存放json文件的路径  ps:目录中只能存放json文件
    xml_path = r"/home/zhang/下载/SEG_task/Annotation/O_11_xml"  # 该目录为放xml文件的路径
    json_to_xml(json_path, xml_path)
