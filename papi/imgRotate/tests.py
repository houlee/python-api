# -*- coding: utf-8 -*-
#from rotate import rotate, figureDegree
from ocr import ocr
import cv2
import requests
import sys
sys.path.append("..") #         这句是为了导入_config
import mylog

logger = mylog.Logger(logname='../log/imgRotate_test.log', loglevel=1, logger="hou").getlog()

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
    #url= 'http://127.0.0.1:8000/imgOcr/'
    url= 'http://papi.nb.com/imgOcr/'
    #url_list=['http://file.fengkuangtiyu.cn/old/images/900/90015759818226579334.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759818216084494.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759818918131785.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759818019831903.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015759144144043760.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015758418141947957.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756942297074845.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756508813261853.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756382795891839.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015756382141356461.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015718049603469182.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015742476088588479.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015740783413702498.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015739062897325164.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015750235922624129.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015749386814174360.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015747684238389457.jpg','http://file.fengkuangtiyu.cn/old/images/900/90015747683640417640.jpg']
    url_list=['http://file.fengkuangtiyu.cn/old/images/900/90015759818226579334.jpg','https://public.zgzcw.com/d/images/201910291572328653220_872.png']
    #url_list = ['./imgRotate/img/test19.jpg']
    for u in url_list:
        data = {'url': u, 'type': 1}
        # data = {'url': "./imgRotate/img/test19.jpg", 'type': 1}
        h = requests.post(url, json=data)
        logger.info('test03:{0}'.format(h.text))


''' 
#测试链接
http://file.fengkuangtiyu.cn/old/images/900/90015759818226579334.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015759818216084494.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015759818918131785.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015759818019831903.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015759144144043760.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015758418141947957.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015756942297074845.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015756508813261853.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015756382795891839.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015756382141356461.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015718049603469182.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015742476088588479.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015740783413702498.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015739062897325164.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015750235922624129.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015749386814174360.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015747684238389457.jpg
http://file.fengkuangtiyu.cn/old/images/900/90015747683640417640.jpg
'''
def test04():
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




if __name__ == '__main__':
    #test01()
    #test02()
    test03()
    #test04()




