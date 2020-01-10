# -*- coding: utf-8 -*-
from .utils import image_read
from .gif_logo import  get_gif_frame1,hsv_mask
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
import os
import cv2
from . import ac

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
    #gif 解包     https://blog.csdn.net/qq_34440148/article/details/100667403     https://www.cnblogs.com/fly-kaka/p/11694011.html

    #图片匹配logo位置     https://www.zhangshengrong.com/p/w4N7BxkJar/            https://www.helplib.cn/fansisi/aircv

    #图片去logo

    #组装gif      https://blog.csdn.net/monotonomo/article/details/80586194


    return Response({'data': results})


@csrf_exempt
@api_view(http_method_names=['post'])                #只允许 post
@permission_classes((permissions.AllowAny,))
#定位图片上水印logo位置      https://www.zhangshengrong.com/p/w4N7BxkJar/            https://www.helplib.cn/fansisi/aircv
#输入：picurl  待处理pic地址；logourl   logo样本地址；matchtype  0  模板匹配（完全匹配）   1   特征点匹配（模糊匹配）
#channel 1：直播吧   2：虎扑
#输出：pic中logo的坐标
def pic_logo_location(request):
    parameter = request.data
    logger.info('logo_location para:{0}'.format(parameter))
    pic_path = parameter['picurl']
    logo_path = parameter['logourl']
    matchtype = parameter['matchtype']
    channel = parameter['channel']

    if pic_path.find('gif') != -1:
        #gif 取首帧图片
        logger.info('logo_location get gif')
        imsrc = get_gif_frame1(pic_path)
    else:
        imsrc = image_read(pic_path)
    if channel==1:
        #直播吧取左下四分之一图像
        logger.info('logo_location zbb 1/4')
        height, width = imsrc.shape[:2]
        imsrc = imsrc[height // 2:height, 0:width // 2]
    imlogo = image_read(logo_path)

    #hsv mask
    imsrc = hsv_mask(imsrc, channel)
    imlogo = hsv_mask(imlogo, channel)
    # find the match position
    if matchtype == 1:
        #特征点匹配
        logger.info('logo_location find_sift')
        try:
            results = ac.find_sift(imsrc, imlogo)
        except Exception as e:
            logger.error('logo_location find_template error:{0}'.format(e))
            logger.error('logo_location find_sift error! picurl:{0}; logourl:{1}'.format(pic_path,logo_path))
            results = []
    else:
        logger.info('logo_location find_template')
        try:
            results = ac.find_template(imsrc, imlogo)
            # 交换rectangle 2，3点的位置，符合左上左下右下右上的顺序
            rec = list(results['rectangle'])
            tmp = rec[2]
            rec[2] = rec[3]
            rec[3] = tmp
            results['rectangle'] = tuple(rec)
        except Exception as e:
            logger.error('logo_location find_template error:{0}'.format(e))
            #logger.error('logo_location find_template error traceback:{0}'.format(traceback.format_exc()))
            logger.error('logo_location find_template error! picurl:{0}; logourl:{1}'.format(pic_path, logo_path))
            results = []

    #results = pos['rectangle']      #矩形坐标
    #results = pos['result']         #中心坐标
    logger.info('logo_location position:{0}'.format(results))
    if channel==1:
        #直播吧恢复坐标，从左下四分之一图像
        # 恢复矩形坐标
        rectangle = []
        for item in results['rectangle']:
            a = list(item)
            a[1] = a[1] + height // 2
            a = tuple(a)
            rectangle.append(a)
        # 恢复中心坐标
        center = list(results['result'])
        center[1] = center[1] + height // 2
        center = tuple(center)

        results['result'] = center
        results['rectangle'] = rectangle
        logger.info('logo_location position zbb:{0}'.format(results))

    return Response({'data': results})