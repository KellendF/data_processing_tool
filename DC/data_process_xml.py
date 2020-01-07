'''
    数据处理
    先遍历文件夹下所有文件根据json文件的图片名称拼接图片完整路径，读取同名图片计算md5值，
    将md5值与当前类型数据库那么字段进行比对存在则将当前的同名文件其他格式删除，不存在则
    将该文件信息写入数据库并且改变同名其他类型文件名称为该图片的md5值
'''
import os
import sqlite3
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET



class Data(object):
    def __init__(self,table,source,data_type,file_type,describe=None):
        self.table = table
        self.source = source
        self.describe = describe
        self.file_type = file_type
        self.data_type = data_type
        self.num = 0
        self.same_num = 0
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()


    def get_file(self,path):
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

    def get_file_info(self,file_path):
        '''
        校验文件计算md5值
        @param file_path: 文件完整路径
        @return: 该文件的md5值
        '''
        md5 = hashlib.md5()
        try:
            with open(file_path,'rb') as f:
                while True:
                    fd = f.read(1024)
                    if not fd:
                        break
                    md5.update(fd)
            return md5.hexdigest()
        except:
            return None

    def judge_file_to_db(self,value):
        '''
        判断数据库中是否有相同数据
        @param value: 图片md5值
        @param type: 上传的类型（‘部件’，‘损伤’）
        @return: True/False
        '''
        sql = 'select * from %s where name = "%s";'%(self.table,value)
        self.cur.execute(sql)
        if self.cur.fetchone():
            return False
        return True

    def insert_data_to_db(self, name, company, width, height, label_dict):
        '''
        插入数据
        @param name:图片md5值
        @param source: 来源
        @param describe: 描述
        @param company: 公司
        @param file_type: 文件类型（json/xml）
        @param width: 图片宽
        @param height: 图片高
        @param data_type: 数据类型（多边形/画框）
        @return:
        '''
        if self.describe == None:
            sql = 'insert into %s values ("%s","%s","%s","%s","%s",%s,%s)' % (
                self.table, name, self.source, self.data_type, company, self.file_type, width, height)
        else:
            sql = 'insert into %s values ("%s","%s","%s","%s","%s","%s","%s",%s,"%s","%s","%s","%s","%s","%s","%s",%s,%s)' % (
                self.table, name, self.source, self.data_type, company, self.file_type, self.describe, width, height,
                label_dict['guaca'], label_dict['aoxian'], label_dict['huahen'], label_dict['boliposun'],
                label_dict['boliliewen'], label_dict['zhezhou'], label_dict['silie'], label_dict['jichuan'],
                label_dict['queshi'],)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.num += 1
            return True
        except Exception as e:
            print(e, '-->insert  error')
            return False


    def parse_xml_file(self,file_path):
        '''
        获取文件信息
        @param file_path: json文件路径
        @return: 图片名称，图片宽，图片高，公司
        '''
        label_dict = {"boliposun": 0, "boliliewen": 0, "huahen": 0, "guaca": 0, "aoxian": 0, "zhezhou": 0, "silie": 0,
                      "jichuan": 0, "queshi": 0}
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            img_name = root.find('filename').text
            size = root.find('size')
            width = size.find('width').text
            height = size.find('height').text
            company = '精友'
            for object in root.findall('object'):
                label = object.find('name').text
                if label in label_dict.keys():
                    label_dict[label] += 1
            return img_name,width,height,company,label_dict
        except Exception as e:
            print(e,'===',file_path)
            return None,None,None,None,None

    def update_json_xml(self,file_path,new_name):
        '''
        更新json和xml文件呢中图片名称
        @param file_path:
        @param new_name:
        @return:
        '''
        jpg_name = file_path.split('/')[-1].split('.')[0]
        with open(file_path, 'r') as f:
            json_info = f.read()
            new_json_file = json_info.replace(jpg_name, new_name)
        new_xml_path = os.path.dirname(file_path)+'/'+new_name+'.'+jpg_name.split('.')[-1]
        # new_xml_path = file_path.replace(jpg_name,new_name)
        with open(new_xml_path, 'w') as f:
            f.write(new_json_file)
        os.remove(file_path)
        return new_xml_path


    def rename_file(self,path,newname):
        '''
        更改文件名称
        @param path: 文件完整路径,文件新名称
        @return: None
        '''
        file_type = path.split('.')[-1]
        name = newname + '.' + file_type
        oldname = path.split('/')[-1]
        newpath = path.replace(oldname,name,1)
        try:
            os.rename(path,newpath)
        except Exception as e:
            print(e)
        return newpath

    def move_file(self,old_path, new_dir):
        '''
        移动文件
        @param old_path:文件当前路径
        @param new_dir: 新目录
        @return: None
        '''
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_path = new_dir + old_path.split('/')[-1]

        try:
            shutil.move(old_path, new_path)
        except:
            print('{} is error'.format(old_path))

    def copy_file(self,old_path, new_dir):
        '''
        复制文件
        @param old_path:文件当前路径
        @param new_dir: 新目录
        @return: None
        '''
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_path = new_dir + old_path.split('/')[-1]
        try:
            shutil.copyfile(old_path, new_path)
        except:
            print('{} is error'.format(old_path))


    def split_file(self,xml_path,jpg_path):
        '''
        拆分目录下文件分类保存
        @param xml_path:
        @param jpg_path:
        @return:
        '''
        directory = os.path.dirname(xml_path)
        dirname1 = directory+'_jpg_xml/'
        if not os.path.exists(dirname1):
            os.makedirs(dirname1)
        shutil.move(xml_path,os.path.join(dirname1,xml_path.split('/')[-1]))
        shutil.move(jpg_path,os.path.join(dirname1,jpg_path.split('/')[-1]))

    def remove_file(self,path):
        '''
        删除文件
        @param path: 文件完整路径
        @return: None
        '''
        if os.path.exists(path):
            os.remove(path)


    def run(self,path):
        '''

        @param path:
        @return:
        '''
        file_list = self.get_file(path)
        for file_path in file_list:
            if os.path.splitext(file_path)[-1] =='.xml':
                img_name, width, height, company, label_dict = self.parse_xml_file(file_path)
                if img_name:
                    img_path = os.path.join(os.path.dirname(file_path),img_name)
                    img_md5 = self.get_file_info(img_path)
                    if not img_md5:
                        continue
                    if self.judge_file_to_db(img_md5):
                        xml_path = file_path
                        jpg_path = img_path
                        if img_name.split('.')[0] != img_md5:
                            xml_path = self.update_json_xml(file_path,img_md5)
                            jpg_path = self.rename_file(img_path,img_path.replace(img_name,img_md5))
                        self.split_file(xml_path,jpg_path)
                        self.insert_data_to_db(img_md5, company, width, height,label_dict)
                        print(img_name,'----ok')
                    else:
                        # new_dir = '../../train/same_file/'
                        # self.move_file(file_path,new_dir)
                        # self.move_file(img_path,new_dir)
                        # if os.path.exists(xml_path):
                        #     self.move_file(xml_path,new_dir)
                        # self.remove_file(file_path)
                        # self.remove_file(img_path)
                        self.same_num +=1
                        print(img_name,'-----same',img_md5)

        print('本次添加成功图片',self.num,'\n相同图片共',self.same_num)
        self.cur.close()
        self.conn.close()




if __name__ == '__main__':
    path = '../../test'
    da = Data('damage','精友数据','画框','xml','9种损伤')
    # da = Data('part','精友数据','画框','xml')
    da.run(path)




