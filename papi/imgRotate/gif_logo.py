# coding=utf-8
# 图片去水印

import cv2
import numpy as np
from PIL import Image, ImageSequence
from urllib.request import urlretrieve
from .utils import cache_set,cache_get,cache_increase,get_savepath,get_file_content
import os

def showAndWaitKey(winName, img):
    cv2.imshow(winName, img)
    cv2.waitKey()

'''
#暂时不用
def parseGIF(gifname):

    # 将gif解析为图片
    # 读取GIF
    im = Image.open(gifname)
    # GIF图片流的迭代器
    iter = ImageSequence.Iterator(im)
    # 获取文件名
    file_name = gifname.split(".")[0]
    index = 1
    # 判断目录是否存在
    pic_dirct = "imgs/{0}".format(file_name)
    mkdirlambda = lambda x: os.makedirs(
        x) if not os.path.exists(x) else True  # 目录是否存在,不存在则创建
    mkdirlambda(pic_dirct)
    # 遍历图片流的每一帧
    for frame in iter:
        print("image %d: mode %s, size %s" % (index, frame.mode, frame.size))
        frame.save("imgs/%s/frame%d.png" % (file_name, index))
        index += 1

    # frame0 = frames[0]
    # frame0.show()

    # 把GIF拆分为图片流
    imgs = [frame.copy() for frame in ImageSequence.Iterator(im)]
    # 把图片流重新成成GIF动图
    imgs[0].save('out.gif', save_all=True, append_images=imgs[1:])

    # 图片流反序
    imgs.reverse()
    # 将反序后的所有帧图像保存下来
    imgs[0].save('./reverse_out.gif', save_all=True, append_images=imgs[1:])
'''

#获取gif的第一帧图片
def get_gif_frame1(gifurl):

    if gifurl.find('http') != -1:  # 网络图片
        # 获取本地地址
        localpath = get_savepath(gifurl)
        # 保存到本地
        urlretrieve(gifurl, localpath)
        x = cv2.VideoCapture(localpath)
        # 删除临时文件
        os.remove(localpath)

    else:  # 本地图片
        localpath = gifurl
        # 读取gif
        x = cv2.VideoCapture(localpath)

    # 读取首帧
    ret, frame = x.read()
    #if ret == True:
    #    cv2.imshow('1', frame)
    #    cv2.waitKey()
    #    cv2.imwrite('1.png', frame)
    return frame


def remove_logo():
    path = "image/1.png"
    path_dst = "image/1r01.png"

    img = cv2.imread(path)

    #获取logo位置
    img_logo = img[293:323, 157:288]   #get_coordinate中获取的坐标是反的
    showAndWaitKey("img_logo",img_logo)

    hight, width, depth = img_logo.shape[0:3]

    # 图片二值化处理，把[240, 240, 240]~[255, 255, 255]以外的颜色变成0
    thresh = cv2.inRange(img_logo, np.array([240, 240, 240]), np.array([255, 255, 255]))

    # 创建形状和尺寸的结构元素
    kernel = np.ones((3, 3), np.uint8)

    # 扩张待修复区域
    hi_mask = cv2.dilate(thresh, kernel, iterations=1)
    specular = cv2.inpaint(img_logo, hi_mask, 5, flags=cv2.INPAINT_TELEA)

    showAndWaitKey("new img_logo",specular)

    img[293:323, 157:288] = specular    #拼接恢复图像 指定位置填充，大小要一样才能填充
    showAndWaitKey("final",img)

    cv2.imwrite(path_dst, img)      #保存图像
    cv2.destroyAllWindows()

#获取图片上坐标值
def get_coordinate():
    path = "image/1.png"
    path_dst = "image/1r01.png"

    img = cv2.imread(path)

    a = []
    b = []

    def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            a.append(x)
            b.append(y)
            cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            cv2.imshow("image", img)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    print(a[0], b[0])

    img[b[0]:b[1], a[0]:a[1], :] = 0  # 注意是 行，列（y轴的，X轴）
    cv2.imshow("image", img)
    cv2.waitKey(0)
    print(a, b)

#获取图片上HSV值 H：图像的色彩/色度；S：图像的饱和度；V：图像的亮度
HSV = []
def getpos(event,x,y,flags,param):
    global HSV
    if event==cv2.EVENT_LBUTTONDOWN:
        print(HSV[y,x])

def get_hsv(path):
    image=cv2.imread(path)
    global HSV
    HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #th2=cv2.adaptiveThreshold(imagegray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imshow("imageHSV",HSV)
    cv2.imshow('image',image)
    cv2.setMouseCallback("imageHSV",getpos)
    cv2.waitKey(0)

#对特定渠道的图片做HSV屏蔽
#输入 img  读取的图像数据    channel  1：直播吧
#输出 屏蔽后的图像数据
def hsv_mask(img,channel):

    #imsrc = cv2.imread('./imgRotate/img/zbb/zbb-pic01.png')

    # 屏蔽图像
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if channel == 1:
        Lower = np.array([100, 150, 150])
        Upper = np.array([110, 250, 250])
    else:
        #无屏蔽
        Lower = np.array([0, 0, 0])
        Upper = np.array([180, 255, 255])

    mask = cv2.inRange(HSV, Lower, Upper)
    resImg = cv2.bitwise_and(img, img, mask=mask)
    return resImg