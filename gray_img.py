'''
    图片转灰度
'''
import cv2 as cv

from data_to_heavy import *







if __name__ == '__main__':
    path = '../train/邦浩验收/cjf/6440f157c31b74813c66b53fdb0c2cf4.jpg'

    img = cv.imread(path)
    image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # _,image = cv.threshold(imgGray, 127, 255, cv.THRESH_BINARY)
    # print(image/255)
    cv.putText(image, path, (-100, 100), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
    cv.imshow('image', image)
    cv.waitKey()

    '''
    file_list = get_file(path)

    for file_path in file_list:
        if file_path.endswith('.jpg'):
            img = cv.imread(file_path)
            image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            image = image/255
            cv.putText(image,file_path,(-100,100),cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
            cv.imshow('image', image)
            cv.waitKey(3000)

    '''

