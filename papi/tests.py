# -*- coding: utf-8 -*-

from imgRotate import ocr
import cv2

from urllib.request import urlretrieve
import aircv as ac
import requests
import sys
sys.path.append("..")
#import mylog
from imgRotate.global_data import g_debug,g_ocr_type,g_count_bdocr
from imgRotate.utils import cache_get,cache_set,namestr,get_savepath
import os
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
    url_list=['http://file.fengkuangtiyu.cn/old/images/900/90015759818226579334.jpg','https://public.zgzcw.com/d/images/201910291572328653220_872.png']
    #url_list = ['./imgRotate/img/lottery.jpg']
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
    path = "./img/test11.jpeg"
    # savepath = ["./img/test04r01.jpg","./img/test04r02.jpg","./img/test04r03.jpg","./img/test04r04.jpg"]
    # savepath = ["./img/test02r31.jpeg", "./img/test02r32.jpeg", "./img/test02r33.jpeg", "./img/test02r34.jpeg"]
    # savepath = ["./img/test05r01.jpg","./img/test05r02.jpg"]
    savepath = ["./img/test11r01.jpeg"]
    precision = 2
    degree = figureDegree(path, precision)
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
        rotateImg = rotate(path, degree[i])
        showAndWaitKey1("rotateImg", rotateImg)
        cv2.imwrite(savepath[i], rotateImg)
        ocr(savepath[i])

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

    #picurl = './imgRotate/img/zbb-pic02.png'
    picurl = 'https://public.zgzcw.com/d/images/201912301577706608417_872.png'
    #picurl = 'http://wx4.sinaimg.cn/mw690/006ekxoggy1gad56jz0v0g30aa0587wj.gif'
    #logourl = './imgRotate/img/logo_zbb.png'
    logourl = 'https://public.zgzcw.com/d/images/201912301577701547232_872.png'
    data = {'picurl': picurl, 'logourl': logourl, 'matchtype': 1}
    h=requests.post(url,json=data)
    print('test11:{0}'.format(h.text))


# print circle_center_pos
def draw_circle(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('objDetect', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_rectangle(img, pos0, pos3, color, line_width):
    # cv2.rectangle()
    # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
    cv2.rectangle(img, pos0, pos3,color, line_width)
    cv2.imshow('objDetect', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #cv2.imwrite("./aaa.png", img)

def test12():
    imsrc = ac.imread('./imgRotate/img/hupu001.jpg')
    imobj = ac.imread('./imgRotate/img/hupologo01.jpg')

    #imsrc = ac.imread('./imgRotate/img/zbb-pic01.png')
    #imobj = ac.imread('./imgRotate/img/logo_zbb.png')

    # find the match position
    #pos = ac.find_template(imsrc, imobj)
    #pos = ac.find_all_sift(imsrc, imobj,1)
    #try:
    pos = ac.find_sift(imsrc, imobj)
    #except: err
    #    print("find_sift error %s"%err)
    #else:
    print(pos)

    # draw circle
    #circle_center_pos = pos['result']
    #print(circle_center_pos)
    #center = []
    #for p in circle_center_pos:
        #print(type(p))
        #p = int(p)
        #center.append(p)
    #print(center)
    #center_t = tuple(center)        #list 转换为 tuple
    #circle_radius = 50
    #color = (0, 255, 0)
    #line_width = 2
    #draw_circle(imsrc, center_t, circle_radius, color, line_width)

    # draw rectangle
    color = (0, 255, 0)
    line_width = 2
    rectangle = pos['rectangle']
    print(rectangle)
    # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
    draw_rectangle(imsrc, rectangle[0], rectangle[2],color, line_width)
    #draw_rectangle(imsrc, (8,322), (126,352), color, line_width)


print(g_debug)

if __name__ == '__main__':
    #test01()
    #test02()
    #for i in range(30):
        #test03()
    #test04()
    #test05()
    #test10()
    test11()
    #test12()





