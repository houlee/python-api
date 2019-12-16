# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math
from . import utils

#pip install pytesseract，pip install tesseract，pip install tesseract-ocr，
#必须要能识别出线条，否则会报错

#返回出现次数最多的元素
def max_list(lt):
    temp = 0
    for i in lt:
        if lt.count(i) > temp:
            max_str = i
            temp = lt.count(i)
    return max_str

#数据处理，以角度为key，保存出现次数和累计长度 在dict字典里
#dict结构：{degree1:[count1,len1],degree2:[count2,len2]}
def dataProc(dict,precision,x1,y1,x2,y2):
    a = y1 - y2
    b = x1 - x2
    k = float(a) / (b)                      #计算斜率
    degree = np.degrees(math.atan(k))       #计算角度
    degreeM = int(round(degree) / precision) * precision     #角度以precision精度为模进行模化
    #print(k)
    #print(degreeM)
    len = math.sqrt(a ** 2 + b ** 2)          #计算线段长度
    # showAndWaitKey("houghP", drawing)
    # 把角度，次数和累计长度 保存为一个字典，角度为key，次数和累计长度合并为list，作为value，根据次数和长度 分别排序取出key角度，进行旋转
    if degreeM in dict:
        dict[degreeM][0] += 1     #count加 1
        dict[degreeM][1] += len   #len 累加
    else:
        dict.setdefault(degreeM, []).append(1)    # count加 1
        dict.setdefault(degreeM, []).append(len)  # len 累加
    #print("dict: %s" %(dict))


# 使用霍夫变换
#precision 是设置旋转精度，传3，表示最小精度是3度
#返回角度列表，第一个是次数最多的角度，第二个是累计长度最长的角度
def figureDegree(path,precision):
    #判断是否网络图片还是本地图片
    if path.find('http') != -1:         #网络图片
        print("network pic")
        # 读取图片，灰度化
        src = utils.url_to_image(path, cv2.IMREAD_COLOR)
        # showAndWaitKey("src", src)
        gray = utils.url_to_image(path, cv2.IMREAD_GRAYSCALE)
        # showAndWaitKey("gray", gray)
    else:           #本地图片
        print("local pic")
        # 读取图片，灰度化
        src = cv2.imread(path, cv2.IMREAD_COLOR)
        # showAndWaitKey("src", src)
        gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        # showAndWaitKey("gray", gray)

    # 腐蚀、膨胀
    kernel = np.ones((5, 5), np.uint8)
    erode_Img = cv2.erode(gray, kernel)
    eroDil = cv2.dilate(erode_Img, kernel)
    #showAndWaitKey("eroDil", eroDil)
    # 边缘检测
    canny = cv2.Canny(eroDil, 50, 150)
    #showAndWaitKey("canny", canny)
    # 霍夫变换得到线条
    """
    HoughLinesP(image, rho, theta, threshold, lines=None, minLineLength=None, maxLineGap=None) 
    image： 必须是二值图像，推荐使用canny边缘检测的结果图像； 
    rho: 线段以像素为单位的距离精度，double类型的，推荐用1.0 
    theta： 线段以弧度为单位的角度精度，推荐用numpy.pi / 180 
    threshod: 累加平面的阈值参数，int类型，超过设定阈值才被检测出线段，值越大，基本上意味着检出的线段越长，检出的线段个数越少。根据情况推荐先用100试试
    lines：这个参数的意义未知，发现不同的lines对结果没影响，但是不要忽略了它的存在 
    minLineLength：线段以像素为单位的最小长度，根据应用场景设置 
    maxLineGap：同一方向上两条线段判定为一条线段的最大允许间隔（断裂），超过了设定值，则把两条线段当成一条线段，值越大，允许线段上的断裂越大，越有可能检出潜在的直线段
    """
    #lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 40, minLineLength=100, maxLineGap=100)
    #lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 40, minLineLength=100, maxLineGap=200)        #test04,test05ok，precision=3
    lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 40, minLineLength=100, maxLineGap=200)         #对于长度选择模式，都ok，precision=1
    if not lines.any():
        return 0
    drawing = np.zeros(src.shape[:], dtype=np.uint8)
    # 画出线条
    dataDict={}
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(drawing, (x1, y1), (x2, y2), (0, 255, 0), 1, lineType=cv2.LINE_AA)
        #数据处理，保存到字典中
        #print(x1,y1,x2,y2)
        dataProc(dataDict,precision,x1,y1,x2,y2)

    degree=[]
    # dict结构：{degree1:[count1,len1],degree2:[count2,len2]}
    #按长度倒序排序
    lenList = sorted(dataDict.items(), key=lambda x: x[1][1], reverse=True)
    #print("lenList: %s" %(lenList))
    degree.append(lenList[0][0])

    # 按次数倒序排序
    countList = sorted(dataDict.items(), key=lambda x: x[1][0], reverse=True)
    #print("countList: %s" % (countList))
    degree.append(countList[0][0])

    #showAndWaitKey("houghP", drawing)
    """
    计算角度,因为x轴向右，y轴向下，所有计算的斜率是常规下斜率的相反数，我们就用这个斜率（旋转角度）进行旋转
    """
    print("figure degree: %s"%(degree))

    return degree

def rotate(path, angle, center=None, scale=1.0):
    """
    旋转角度大于0，则逆时针旋转（正值），否则顺时针旋转（负值）
    """
    # 判断是否网络图片还是本地图片
    if path.find('http') != -1:  # 网络图片
        # 读取图片
        image = utils.url_to_image(path, cv2.IMREAD_COLOR)
        # showAndWaitKey("src", src)
    else:  # 本地图片
        # 读取图片
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        # showAndWaitKey("src", src)

    # 调整角度
    """
    if (angle == 90) or (angle == -90):
        angle=angle
    elif angle > 60:
        angle = -(90 - angle)
    elif angle < -60:
        angle = 90+angle
    """
    #文字倾斜的情况，一般习惯于左倾，识别范围：左倾100度以内，右倾80度以内，超过80度，都认为是左倾
    if (angle >= 80):
        angle = angle-180

    print("rotate angle:%d" % (angle))
    (w, h) = image.shape[0:2]
    print(w,h)
    if center is None:
        center = (w // 2, h // 2)
    wrapMat = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, wrapMat, (h, w))
    #cv2.putText(rotated, 'Angle: {:.2f} degrees orc-rotate'.format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return rotated


