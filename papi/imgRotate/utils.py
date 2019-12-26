# -*- coding: utf-8 -*-
import cv2
import urllib
import numpy as np
#from imgRotate import logger
from .global_data import g_debug

#日志设置
import logging
logger = logging.getLogger('log')

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
    if g_debug:
        IMAGE_ROOT = "/Users/houlee/Documents/git_dev/python-api/papi/image_temp"  # 本地测试路径
    else:
        IMAGE_ROOT = "/app/python-api/papi/image_temp"

    # 查找文件名后缀位置
    #print("get_savepath")
    #print(path)
    path_list = list(path)
    nPos = path.rfind('.')
    path_list.insert(nPos, "result")
    path1 = "".join(path_list)
    #print(path1)
    if path1.find("http") != -1:  # 网络图片
        nPos1 = path1.rfind('/')
        path2 = IMAGE_ROOT + path1[nPos1:]
        #print(path2)
        return path2
    else:  # 本地图片
        return path1

#字符串转换为字典
def str_to_dict(str):
    d={}
    str1 = str.replace(' ','')  #去空格
    d["words"]=str1
    return d
#组装返回 data 格式
#输入data："第 3 多 周 六 004\n洙 南 海 洋 王 队 : 懵腹小芊 Vs 八\n\n授 注 对 应 的 奖 金 额 )\n7,000.00 五"
#输出data：{"log_id":3091207121918435257,"words_result_num":10,"words_result":[{"words":"第3场周六004"},{"words":"湘南海洋"},{"words":"主队:横滨水手vs"},{"words":"(3:1)10.00元"},{"words":"投注对应的奖金额)"},{"words":"(选顶固定奖金额为"},{"words":",000.00元"},{"words":"本票最高可能固定奖"},{"words":"单倍注数:3×1*1注;共"},{"words":"***"}]}
def package_data(data):
    # 用 \n 分隔字符串，返回列表
    words_result=data.split('\n')
    #删除空值
    while '' in words_result:
        #logger.info("null in words_result")
        words_result.remove('')
    #logger.info("words_result {0}".format(words_result))
    #组装words_result字典列表（使用map函数）
    words_result_r = list(map(str_to_dict, words_result))
    #logger.info("words_result_r {0}".format(words_result_r))
    data_r={}
    data_r["log_id"] = 1
    data_r["words_result_num"] = len(words_result_r)
    data_r["words_result"] = words_result_r
    return data_r