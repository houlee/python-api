# -*- coding: utf-8 -*-
#from . import gif_logo
from .utils import cache_set,cache_get,cache_increase,get_savepath,get_file_content,image_read
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
import os
import cv2
import aircv as ac

#日志设置
import logging
logger = logging.getLogger('log')

@csrf_exempt
@api_view(http_method_names=['post'])                #只允许 post
@permission_classes((permissions.AllowAny,))

#去除gif上水印logo
#输入：gifurl  gif地址；logourl   logo样本地址
#输出：gifurl  去除水印后的gif
def gif_logo_remove(request):
    parameter = request.data
    logger.info('gif_logo_remove para:{0}'.format(parameter))
    #gif 解包     https://www.cnblogs.com/fly-kaka/p/11694011.html

    #图片匹配logo位置     https://www.zhangshengrong.com/p/w4N7BxkJar/            https://www.helplib.cn/fansisi/aircv

    #图片去logo

    #组装gif      https://blog.csdn.net/monotonomo/article/details/80586194


    return Response({'data': results})


@csrf_exempt
@api_view(http_method_names=['post'])                #只允许 post
@permission_classes((permissions.AllowAny,))
#定位图片上水印logo位置      https://www.zhangshengrong.com/p/w4N7BxkJar/            https://www.helplib.cn/fansisi/aircv
#输入：picurl  待处理pic地址；logourl   logo样本地址
#输出：pic中logo的坐标
def pic_logo_location(request):
    parameter = request.data
    logger.info('logo_location para:{0}'.format(parameter))
    pic_path = parameter['picurl']
    logo_path = parameter['logourl']

    imsrc = image_read(pic_path)
    imlogo = image_read(logo_path)

    # find the match position
    results = ac.find_template(imsrc, imlogo)
    #results = pos['rectangle']      #矩形坐标
    #results = pos['result']         #中心坐标
    logger.info('logo_location position:{0}'.format(results))

    return Response({'data': results})