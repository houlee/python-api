# -*- coding: utf-8 -*-
import cv2
import urllib
import numpy as np

#util
# URL到图片
def url_to_image(url,color_type=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    # bytearray将数据转换成（返回）一个新的字节数组
    # asarray 复制数据，将结构化数据转换成ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    image = cv2.imdecode(image, color_type)
    # return the image
    return image

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#根据path生成savepath。 xxxx.jpg 生成  xxxxresult.jpg
def get_savepath(path):
    #IMAGE_ROOT = "/data/image_temp/"
    IMAGE_ROOT = "/Users/houlee/Documents/git_dev/temp/"
    # 查找文件名后缀位置
    print("get_savepath")
    print(path)
    path_list = list(path)
    nPos = path.rfind('.')
    path_list.insert(nPos, "result")
    path1 = "".join(path_list)
    print(path1)
    if path1.find("http") != -1:  # 网络图片
        nPos1 = path1.rfind('/')
        path2 = IMAGE_ROOT + path1[nPos1:]
        print(path2)
        return path2
    else:  # 本地图片
        return path1
