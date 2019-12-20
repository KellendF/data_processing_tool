'''
    视频抽帧
'''

import cv2
import os




# 保存图片的路径
def save_img_path(path):
    savedpath = path.replace('.mp4','') + '/'
    print(savedpath)
    isExists = os.path.exists(savedpath)
    if not isExists:
        os.makedirs(savedpath)
        print('path of %s is build' % (savedpath))

    return savedpath


def load_video(path):
    # 视频帧率12
    fps = 12
    # 保存图片的帧率间隔
    count = 60
    # 开始读视频
    videoCapture = cv2.VideoCapture(path)
    i = 0
    j = 0
    savedpath = save_img_path(path)
    while True:
        success, frame = videoCapture.read()
        i += 1
        if (i % count == 0):
            # 保存图片
            j += 1
            savedname = path.split('/')[-1].split('.')[0]+ '_{}.jpg'.format(j)
            cv2.imwrite(savedpath + savedname, frame)
            print('image of %s is saved' % (savedname))
        if not success:
            print('video is all read')
            break


if __name__ == '__main__':
    load_video('../test/car1.mp4')
    # main_path = '../test'
    # path = '../test/care.mp4'
    # print(main_path.split(os.path.sep)[-1])