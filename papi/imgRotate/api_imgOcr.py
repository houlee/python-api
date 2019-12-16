# -*- coding: utf-8 -*-
from . import rotate
from . import utils
import cv2
import pytesseract
from PIL import Image
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from aip import AipOcr
import os
from imgRotate import logger


@csrf_exempt
@api_view(http_method_names=['post'])                #只允许 post
@permission_classes((permissions.AllowAny,))

#倾斜图片校正角度，返回校正后的图片地址
def img_rotate(request):
    parameter = request.data
    logger.info('img_rotate para:{0}'.format(parameter))
    #获取原始图片地址
    #val = os.system('ls ./imgRotate/img/test11.jpg')         #当前位置为项目根目录
    #print(val)
    path = parameter['url']
    precision = 2
    #计算旋转角度并旋转。 degree[0] 累计长度最长；degree[0] 累计次数最多
    degree = rotate.figureDegree(path, precision)
    rotateImg = rotate.rotate(path, degree[0])
    logger.info('rotate degree:{0}'.format(degree[0]))
    #上传图片

    #获取图片地址并返回
    return Response({'picdata':rotateImg})
    #return Response({'dstpath':dstpath})

@csrf_exempt
@api_view(http_method_names=['post'])                #只允许 post
@permission_classes((permissions.AllowAny,))
#图片OCR接口 识别文字，返回识别后的文字。type取值 1：百度OCR; 2: 疯狂OCR
def img_ocr(request):

    parameter = request.data
    logger.info('img_ocr para:{0}'.format(parameter))

    #获取原始图片地址
    path = parameter['url']
    type = parameter['type']
    precision = 2
    #计算旋转角度并旋转。 degree[0] 累计长度最长；degree[0] 累计次数最多
    degree = rotate.figureDegree(path, precision)
    rotateImg = rotate.rotate(path, degree[0])

    #获取保存图片地址并保存旋转后的图片
    savepath=utils.get_savepath(path)
    cv2.imwrite(savepath, rotateImg)

    if type == 2:
        #logger.info('FKocr')
        results=FKocr(savepath)
    else:
        #logger.info('BDocr')
        results=BDocr(savepath)
    logger.info('ocr results:{0}'.format(results))
    results1 = BDocr(path)
    logger.info('ori ocr results:{0}'.format(results1))

    #删除旋转后的临时文件
    os.remove(savepath)
    #OCR
    # pip install pytesseract，pip install tesseract，pip install tesseract-ocr，
    # 必须要能识别出线条，否则会报错
    return Response({'data': results})
#
def FKocr(path):
    # image = Image.open("./img/test04r01.jpg")
    image = Image.open(path)
    # 对图片进行阈值过滤（低于143的置为黑色，否则为白色）
    # 相当于对电脑显卡调节对比度(电脑显卡对比度默认为50,我比较习惯于调成53)
    image = image.point(lambda x: 0 if x < 143 else 255)
    # 重新保存图片
    image.save(path)
    code = pytesseract.image_to_string(image, lang='chi_sim')
    logger.info('FKocr results:{0}'.format(code))
    return code


#调用百度图片OCR 识别图片文字，返回识别后的文字
def BDocr(url):

    #百度参数
    """ 你的 APPID AK SK """
    APP_ID = '18032299'
    API_KEY = 'a8a51zBfDGIAH4OGC5LOlF8t'
    SECRET_KEY = 'NFfb6YpLNpGGQnjSGzxoI3KUQozBVPdl'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    #options["detect_direction"] = "true"
    #options["detect_language"] = "true"
    #options["probability"] = "true"

    # 判断是否网络图片还是本地图片
    if url.find('http') != -1:  # 网络图片
        #print("BDocr network pic")
        """ 带参数调用通用文字识别, 图片参数为远程url图片 """
        results = client.basicGeneralUrl(url, options)

    else:  # 本地图片
        #print("BDocr local pic")
        """ 读取图片 """
        image = utils.get_file_content(url)
        """ 带参数调用通用文字识别, 图片参数为本地图片 """
        results = client.basicGeneral(image, options)  # 普通版  每天免费5万次
        # results = client.basicAccurate(image, options)      #高精度版   每天免费500次

    #print(results)
    return results
