# -*- coding: utf-8 -*-

from imgRotate import ocr
import cv2
import numpy as np
from imgRotate import rotate
from imgRotate import gif_logo
from urllib.request import urlretrieve
from imgRotate import ac
import requests
import sys
sys.path.append("..")
#import mylog
from imgRotate.global_data import g_debug,g_ocr_type,g_count_bdocr
from imgRotate.utils import cache_get,cache_set,namestr,get_savepath
import os
#from matplotlib import pyplot as plt
#日志设置
import logging
logger = logging.getLogger('log')

def showAndWaitKey1(winName, img):
    cv2.imshow(winName, img)
    cv2.waitKey()


def test01():
    url= 'http://127.0.0.1:8000/test/'
    data = {'data':2}
    h=requests.post(url,json=data)
    logger.info('test01:{0}'.format(h.text))

def test02():
    url= 'http://127.0.0.1:8000/imgRotate/'
    # http://file.fengkuangtiyu.cn/old/images/900/90015759818216084494.jpg
    data ={'url':"./imgRotate/img/test11.jpg"}
    h = requests.post(url, json=data)
    logger.info('test02:{0}'.format(h.text))

def test03():
    if g_debug:
        url = 'http://127.0.0.1:8000/imgOcr/'
    else:
        url = 'http://papi.nb.com/imgOcr/'

    #url_list=['http://file.fengkuangtiyu.cn/old/images/900/90015759818226579334.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759818216084494.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759818918131785.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759818019831903.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759144144043760.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015758418141947957.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756942297074845.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756508813261853.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756382795891839.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756382141356461.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015718049603469182.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015742476088588479.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015740783413702498.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015739062897325164.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015750235922624129.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015749386814174360.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015747684238389457.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015747683640417640.jpg']
    #url_list=['http://file.fengkuangtiyu.cn/old/images/900/90015759818226579334.jpg','https://public.zgzcw.com/d/images/201910291572328653220_872.png']
    url_list = ['./imgRotate/img/test11.png']
    for u in url_list:
        data = {'url': u, 'type': 1}
        # data = {'url': "./imgRotate/img/test19.jpg", 'type': 1}
        h = requests.post(url, json=data)
        print('test03:{0}'.format(h.text))


def test04():
    global g_ocr_type
    global g_count_bdocr
    g_ocr_type = 1
    g_count_bdocr = 0
    print("jobjobjob")
    os.popen("touch /Users/houlee/Documents/git_dev/python-api/papi/1.txt")
    print("*** job resetData *** g_ocr_type={0}, g_count_bdocr={1}".format(g_ocr_type,g_count_bdocr))

def test05():
    path = "./imgRotate/img/aaa.png"
    # savepath = ["./img/test04r01.jpg","./img/test04r02.jpg","./img/test04r03.jpg","./img/test04r04.jpg"]
    # savepath = ["./img/test02r31.jpeg", "./img/test02r32.jpeg", "./img/test02r33.jpeg", "./img/test02r34.jpeg"]
    # savepath = ["./img/test05r01.jpg","./img/test05r02.jpg"]
    savepath = ["./imgRotate/img/aaar01.png"]
    precision = 3
    degree = rotate.figureDegree(path, precision)
    '''
    #四次旋转
    for i in range(len(savepath)):
        if i==0:
            tmpDegree=degree
            tmpPath=path
        else:
            tmpDegree=-90
            tmpPath=savepath[i-1]
        rotateImg = rotate(tmpPath, tmpDegree)
        showAndWaitKey("rotateImg", rotateImg)
        cv2.imwrite(savepath[i], rotateImg)
        ocr(savepath[i])
    '''
    # 单次旋转或两次
    for i in range(len(savepath)):
        rotateImg = rotate.rotate(path, degree[i])
        showAndWaitKey1("rotateImg", rotateImg)
        cv2.imwrite(savepath[i], rotateImg)
        ocr.ocr(savepath[i])

    cv2.destroyAllWindows()

### test code

def test10():
    global g_ocr_type
    global g_count_bdocr
    print("*** job resetData init *** ")

    # 从 django cache读取变量
    g_ocr_type = cache_get("g_ocr_type")
    g_count_bdocr = cache_get("g_count_bdocr")

    print("*** job resetData *** ")
    print("*** job resetData before *** g_ocr_type={0}, g_count_bdocr={1}".format(g_ocr_type, g_count_bdocr))

    # 重置变量
    g_ocr_type = cache_set("g_ocr_type", 2)
    g_count_bdocr = cache_set("g_count_bdocr", 0)
    g_ocr_type = cache_get("g_ocr_type")
    g_count_bdocr = cache_get("g_count_bdocr")
    # os.popen("touch /Users/houlee/Documents/git_dev/python-api/papi/1.txt")
    print("*** job resetData after *** g_ocr_type={0}, g_count_bdocr={1}".format(g_ocr_type, g_count_bdocr))
    print("*** job resetData *** ")

def test11():
    if g_debug:
        url = 'http://127.0.0.1:8000/logoLocate/'
    else:
        url = 'http://papi.nb.com/logoLocate/'

    #picurl = './imgRotate/img/zbb-pic05.png'
    #picurl = 'https://public.zgzcw.com/d/images/201912301577706608417_872.png'
    picurl = 'http://wx1.sinaimg.cn/mw690/006foVpjgy1gauh470dvmg309l04rqv7.gif'
    #picurl = 'http://wx1.sinaimg.cn/mw690/006ekxoggy1gad3dx86y2g30aa058kjl.gif'
    logourl = './imgRotate/img/zbb-logo01.png'
    #logourl = 'https://public.zgzcw.com/d/images/201912301577701547232_872.png'
    data = {'picurl': picurl, 'logourl': logourl, 'matchtype': 1,'channel':1}
    h=requests.post(url,json=data)
    print('test11:{0}'.format(h.text))


# print circle_center_pos
def draw_circle(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('objDetect', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_rectangle(img, pos0, pos2, color, line_width):
    # cv2.rectangle()
    # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
    cv2.rectangle(img, pos0, pos2,color, line_width)
    cv2.imshow('objDetect', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    #cv2.imwrite("./aaa.png", img)

def test12():
    #imsrc1 = ac.imread('./imgRotate/img/hupu001.jpg')
    #imobj1 = ac.imread('./imgRotate/img/hupologo01.jpg')
    #imsrc = gif_logo.hsv_mask(imsrc1,2)
    #imobj = gif_logo.hsv_mask(imobj1,2)
    imsrc1 = gif_logo.get_gif_frame1('http://wx4.sinaimg.cn/mw690/71a4f909gy1gank3de9c0g20b105mhdv.gif')
    #imsrc1 = ac.imread('./imgRotate/img/zbb-pic08.png')
    imobj1 = ac.imread('./imgRotate/img/zbb-logo01.png')

#取四分之一图像
    height, width = imsrc1.shape[:2]
    print(height)
    print(width)
    imsrc2 = imsrc1[height // 2:height, 0:width // 2]
    cv2.imshow('quater', imsrc2)
    cv2.waitKey()

    imsrc = gif_logo.hsv_mask(imsrc2,1)
    imobj = gif_logo.hsv_mask(imobj1,1)
    # find the match position
    pos = ac.find_sift(imsrc, imobj)
    print(pos)

    # draw rectangle
    color = (0, 255, 0)
    line_width = 2
    rectangle = pos['rectangle']
    print(rectangle)
    cv2.imshow('mask', imsrc)
    cv2.waitKey()

    #恢复坐标
    rectangle = []  # 矩形坐标
    for item in pos['rectangle']:
        a = list(item)
        a[1]=a[1]+height // 2
        a=tuple(a)
        rectangle.append(a)
    center = list(pos['result'])  # 中心坐标
    center[1]=center[1]+height // 2
    center=tuple(center)
    pos['result']=center
    pos['rectangle'] = rectangle
    print(rectangle)
    print(center)



    # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
    draw_rectangle(imsrc1, rectangle[0], rectangle[2],color, line_width)
    #draw_rectangle(imsrc, (8,322), (126,352), color, line_width)

def test121():
    #imsrc1 = ac.imread('./imgRotate/img/hupu001.jpg')
    #imobj1 = ac.imread('./imgRotate/img/hupologo01.jpg')
    #imsrc = gif_logo.hsv_mask(imsrc1,2)
    #imobj = gif_logo.hsv_mask(imobj1,2)
    imsrc1 = gif_logo.get_gif_frame1('http://wx1.sinaimg.cn/mw690/006foVpjgy1gauh470dvmg309l04rqv7.gif')
    #imsrc1 = ac.imread('./imgRotate/img/zbb-pic08.png')
    imobj1 = ac.imread('./imgRotate/img/zbb-logo01.png')

#取四分之一图像
    #直播吧取左下四分之一图像
    height_pic, width_pic = imsrc1.shape[:2]
    print("heightpic %d;widthpic %d"%(height_pic,width_pic))
    imsrc2 = imsrc1[height_pic // 2:height_pic, 0:width_pic // 2]
    height_logo, width_logo = imobj1.shape[:2]
    print("height_logo %d;width_logo %d" % (height_logo, width_logo))
    cv2.imshow('quater', imsrc2)
    cv2.waitKey()

    imsrc = gif_logo.hsv_mask(imsrc2,1)
    imobj = gif_logo.hsv_mask(imobj1,1)

    cv2.imshow('mask', imsrc)
    cv2.waitKey()

    # find the match position
    pos = ac.find_sift(imsrc, imobj)
    print(pos)

    #恢复坐标
    if pos == None:
        return pos
    results00 = gif_logo.co_quarter2full(width_pic, height_pic, pos)
    print("results00:%s"%(results00))

    # 画中心点
    point = results00['result']
    point_size = 1
    color = (0, 0, 255)  # BGR
    thickness = 4  # 可以为 0 、4、8
    cv2.circle(imsrc1, point, point_size, color, thickness)

    # draw rectangle
    # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
    color = (0, 255, 0)
    line_width = 2
    rectangle = results00['rectangle']
    draw_rectangle(imsrc1, rectangle[0], rectangle[2], color, line_width)

    # 以center为中心，按logo 2倍大小生成返回的矩形坐标
    factor = 0.7  # 缩放比例
    results01 = gif_logo.gen_coordinate_from_center(width_logo, height_logo, width_pic, height_pic, results00,factor)
    print("results01:%s"%(results01))

    # draw rectangle
    # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细

    color = (255, 0, 0)
    rectangle = results01['rectangle']
    draw_rectangle(imsrc1, rectangle[0], rectangle[2], color, line_width)

def test13():
    #imsrc = ac.imread('./imgRotate/img/hupu001.jpg')
    #imobj = ac.imread('./imgRotate/img/hupologo01.jpg')
    imsrc1 = gif_logo.get_gif_frame1('http://wx4.sinaimg.cn/mw690/71a4f909gy1gank3de9c0g20b105mhdv.gif')

    #imsrc1 = cv2.imread('./imgRotate/img/zbb-pic04.png')
    imobj1 = cv2.imread('./imgRotate/img/zbb-logo03.png')

    imsrc = gif_logo.hsv_mask(imsrc1,1)
    imobj = gif_logo.hsv_mask(imobj1,1)

    sift = cv2.xfeatures2d.SIFT_create(edgeThreshold=100)  # 创建sift检测器
    kp1, des1 = sift.detectAndCompute(imobj, None)
    kp2, des2 = sift.detectAndCompute(imsrc, None)
    # 设置Flannde参数
    FLANN_INDEX_KDTREE = 0
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)
    matches = flann.knnMatch(des1, des2, k=2)
    # 设置好初始匹配值
    matchesMask = [[0, 0] for i in range(len(matches))]
    for i, (m, n) in enumerate(matches):
        #print("m:%d"%(m.distance))
        #print("n:%d" % (n.distance))
        if m.distance < 0.9 * n.distance:  # 舍弃小于0.5的匹配结果
            print("mmok")
            matchesMask[i] = [1, 0]

    drawParams = dict(matchColor=(0, 0, 255), singlePointColor=(255, 0, 0), matchesMask=matchesMask,
                      flags=0)  # 给特征点和匹配的线定义颜色
    resultimage = cv2.drawMatchesKnn(imobj, kp1, imsrc, kp2, matches, None, **drawParams)  # 画出匹配的结果
    plt.imshow(resultimage, ), plt.show()

def test14():
    # imsrc = ac.imread('./imgRotate/img/hupu001.jpg')
    #imobj = ac.imread('./imgRotate/img/hupologo01.jpg')

    imsrc = cv2.imread('./imgRotate/img/zbb/zbb-logo03.png')
    #imobj = cv2.imread('./imgRotate/img/zbb/zbb-logo02.png')

    #获取图像HSV范围
    #gif_logo.get_hsv('./imgRotate/img/zbb/zbb-logo02.png')
    # 屏蔽图像
    HSV = cv2.cvtColor(imsrc, cv2.COLOR_BGR2HSV)
    #LowerZBB = np.array([100, 150, 210])
    #UpperZBB = np.array([110, 170, 250])
    LowerZBB = np.array([100, 150, 150])
    UpperZBB = np.array([110, 250, 250])
    mask = cv2.inRange(HSV, LowerZBB, UpperZBB)
    ZBBThings = cv2.bitwise_and(imsrc, imsrc, mask=mask)
    cv2.imshow('imsrc',imsrc)
    cv2.imshow('mask',mask)
    cv2.imshow('ZBBThings',ZBBThings)
    cv2.waitKey(0)

def test20():
    if g_debug:
        url = 'http://127.0.0.1:8000/static/'
    else:
        url = 'http://papi.nb.com/static/'

    h=requests.get(url)
    print('test20:{0}'.format(h.text))

print(g_debug)

if __name__ == '__main__':
    #test01()
    #test02()
    #for i in range(30):
        #test03()
    #test04()
    #test05()
    #test10()
    test11()       #test pic logo api
    #test12()       #test pic logo gif_logo function
    #test121()       #test pic logo gif_logo function
    #test13()       #test pic logo local
    #test14()
    #test20()





