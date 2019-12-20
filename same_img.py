'''
    图像相似度检测
'''
import os
import cv2 as cv
from skimage.measure import compare_ssim

EXT = ['.jpg', '.jpeg']


def delete(imgs_n):
    for image in imgs_n:
        os.remove(image)


def find_sim_images(dir_path):
    imgs_n = []
    img_files = [os.path.join(rootdir, file)
    for rootdir, _, files in os.walk(dir_path) for file in files if
                 (os.path.splitext(file)[-1] in EXT)]
    for currIndex, filename in enumerate(img_files):
        if filename in imgs_n:
            continue
        if currIndex >= len(img_files) - 1:
            break
        for filename2 in img_files[currIndex + 1:]:
            if filename2 in imgs_n:
                continue
            img = cv.imread(filename)
            img1 = cv.imread(filename2)
            try:
                ssim = compare_ssim(img, img1, multichannel=True)
                if ssim > 0.9:
                    imgs_n.append(filename2)
                    print(filename, filename2, ssim)
            except ValueError:
                pass
    print(imgs_n)
    return imgs_n


if __name__ == '__main__':
    path = '../test'
    find_sim_images(path)
    # delete(find_sim_images(path))
