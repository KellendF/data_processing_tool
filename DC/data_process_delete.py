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


class Data(object):
    def __init__(self, table, source, data_type, file_type, describe=None):
        self.table = table
        self.source = source
        self.describe = describe
        self.file_type = file_type
        self.data_type = data_type
        self.num = 0
        self.same_num = 0
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()

    def get_file(self, path):
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

    def get_file_info(self, file_path):
        '''
        校验文件计算md5值
        @param file_path: 文件完整路径
        @return: 该文件的md5值
        '''
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                fd = f.read(1024)
                if not fd:
                    break
                md5.update(fd)
        return md5.hexdigest()

    def judge_file_to_db(self, table, value):
        '''
        判断数据库中是否有相同数据
        @param value: 图片md5值
        @param type: 上传的类型（‘部件’，‘损伤’）
        @return: True/False
        '''
        sql = 'select * from %s where name = "%s";' % (table, value)
        self.cur.execute(sql)
        if self.cur.fetchone():
            return False
        return True

    def delete_data_to_db(self, name,table):
        '''
        插入数据
        @param name:图片md5值
        @return:
        '''
        sql = 'delete from %s where name="%s"'%(table,name)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.num += 1
        except Exception as e:
            print(e, '-->delete  error',table)

    def parse_json_file(self, file_path):
        '''
        获取文件信息
        @param file_path: json文件路径
        @return: 图片名称，图片宽，图片高，公司
        '''
        with open(file_path, 'r') as f:
            try:
                dict_info = json.loads(f.read())
                img_name = dict_info['imagePath']
                for label_ in dict_info['shapes']:
                    label = label_['label']
                    if label == 'wuxulabel':
                        return img_name
            except Exception as e:
                print(e, '======', file_path, 'error')
                return None


    def update_json_xml(self, file_path, new_name):
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
        new_json_path = file_path.replace(jpg_name, new_name)
        with open(new_json_path, 'w') as f:
            f.write(new_json_file)
        os.remove(file_path)
        xml_path = file_path.replace('.json', '.xml')
        if xml_path:
            if os.path.exists(xml_path):
                with open(xml_path, 'r') as f:
                    xml_info = f.read()
                    new_xml_file = xml_info.replace(jpg_name, new_name)
                new_xml_path = xml_path.replace(jpg_name, new_name)
                with open(new_xml_path, 'w') as f:
                    f.write(new_xml_file)
                os.remove(xml_path)
                return new_json_path, new_xml_path
        return new_json_path, None

    def rename_file(self, path, newname):
        '''
        更改文件名称
        @param path: 文件完整路径,文件新名称
        @return: None
        '''
        file_type = path.split('.')[-1]
        name = newname + '.' + file_type
        oldname = path.split('/')[-1]
        newpath = path.replace(oldname, name, 1)
        try:
            os.rename(path, newpath)
        except Exception as e:
            print(e)
        return newpath

    def move_file(self, old_path, new_dir):
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

    def copy_file(self, old_path, new_dir):
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

    def split_file(self, json_path, jpg_path,img_md5):
        '''
        拆分目录下文件分类保存
        @param json_path:
        @param xml_path:
        @param jpg_path:
        @return:
        '''
        directory = os.path.dirname(json_path)
        dirname = directory + '_wuxiao/'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        shutil.move(json_path, dirname)
        shutil.move(jpg_path, dirname)
        img_name = jpg_path.split('/')[-1]
        xml_path = '../../train/jpg_xml/' + img_md5 + '.xml'
        xml_jpg_path = '../../train/jpg_xml/' + img_name
        if os.path.exists(xml_path):
            shutil.move(xml_path, dirname)
            os.remove(xml_jpg_path)

    def remove_file(self, path):
        '''
        删除文件
        @param path: 文件完整路径
        @return: None
        '''
        if os.path.exists(path):
            os.remove(path)

    def process_wuxiao_file(self,file_path,img_path):
        '''
        处理wuxulabel的文件
        @param file_path:
        @param img_path:
        @return:
        '''
        dir_path = os.path.dirname(file_path)+'_wuxiao/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        shutil.move(file_path,dir_path)
        shutil.move(img_path,dir_path)
        img_name = img_path.split('/')[-1]
        xml_path = '../train/jpg_xml/'+img_name.split('.')[0]+'.xml'
        xml_jpg_path = '../train/jpg_xml/'+img_name
        if os.path.exists(xml_path):
            shutil.move(xml_path,dir_path)
            os.remove(xml_jpg_path)

    def run(self, path):
        '''
        启动任务
        @param path:
        @return:
        '''
        file_list = self.get_file(path)
        for file_path in file_list:
            if os.path.splitext(file_path)[-1] == '.json':
                img_name = self.parse_json_file(file_path)
                if img_name:
                    img_path = os.path.join(os.path.dirname(file_path), img_name)
                    print(file_path)
                    img_md5 = self.get_file_info(img_path)
                    json_path = file_path
                    jpg_path = img_path
                    self.split_file(json_path, jpg_path,img_md5)
                    self.delete_data_to_db(img_md5,'part')
                    self.delete_data_to_db(img_md5,'damage')
                    print(img_name, '----process ok')

        print('本次删除成功图片', self.num, '\n相同图片共', self.same_num)
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    path = '../../test'
    # da = Data('damage','09年修理厂采集','多边形','json/xml','9种损伤')
    da = Data('part', '第三方公司采集的视频抽帧', '多边形', 'json/xml')
    da.run(path)
