# -*- coding: utf-8 -*-
import cv2
import urllib
import numpy as np
import uuid
from django.core.cache import cache
from .global_data import g_debug
import ssl
context = ssl._create_unverified_context()
#日志设置
import logging
logger = logging.getLogger('log')

#util
# URL到图片
def url_to_image(url,color_type=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url,context=context)
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

#图片读取方法，兼容网络地址和本地地址
#输入：path 图片地址，flag  同cv2.imread的flag参数  cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCALE
#输出：cv2.imread的输出
def image_read(path,flags=cv2.IMREAD_COLOR):
    # 判断是否网络图片还是本地图片
    if path.find('http') != -1:  # 网络图片
        # print("network pic")
        # 读取图片
        src = url_to_image(path, flags)
        # showAndWaitKey("src", src)
    else:  # 本地图片
        # print("local pic")
        # 读取图片，灰度化
        src = cv2.imread(path, flags)
        # showAndWaitKey("src", src)
    return src


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

#字符串转换为字典--不去空格
def str_to_dict(str):
    d={}
    d["words"]=str
    return d
#字符串转换为字典 去空格
def str_to_dict1(str):
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

#获取变量的名字字符串
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] == obj]

####################################################################################
#django cache #
####################################################################################
class CacheLock(object):
    def __init__(self, expires=60, wait_timeout=0):
        self.cache = cache
        self.expires = expires  # 函数执行超时时间
        self.wait_timeout = wait_timeout  # 拿锁等待超时时间

    def get_lock(self, lock_key):
        # 获取cache锁
        #logger.info("get_lock")
        wait_timeout = self.wait_timeout
        identifier = uuid.uuid4()
        while wait_timeout >= 0:
            if self.cache.add(lock_key, identifier, self.expires):
                #logger.info("get_lock identifier:{0}".format(identifier))
                return identifier
            wait_timeout -= 1
            time.sleep(1)
        raise LockTimeout({'msg': '当前有其他用户正在编辑该采集配置，请稍后重试'})

    def release_lock(self, lock_key, identifier):
        # 释放cache锁
        lock_value = self.cache.get(lock_key)
        if lock_value == identifier:
            #logger.info("release_lock lock_value:{0}".format(lock_value))
            self.cache.delete(lock_key)

def lock(cache_lock):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            lock_key = 'bk_monitor:lock:xxx' # 具体的lock_key要根据调用时传的参数而定
            identifier = cache_lock.get_lock(lock_key)
            try:
                return func(*args, **kwargs)
            finally:
                cache_lock.release_lock(lock_key, identifier)
        return wrapper
    return my_decorator

#key 参数   val 参数的值
@lock(CacheLock())
def cache_set(key,val):
    #str = namestr(var,globals())
    #print("key: %s"%(key))
    #cache.set(key,val,300)     #300秒过期
    cache.set(key, val,2*24*60*60)         #2天不过期
    #logger.debug("cache_set: {0} value is {1}".format(key, val))
    return val

#key 参数   key 如果不存在，则返回none
@lock(CacheLock())
def cache_get(key):
    #str = namestr(var, globals())
    val = cache.get(key)
    #logger.debug("cache_get: {0} value is {1}".format(key, val))
    return val

#key 参数   val 参数变动的值
@lock(CacheLock())
def cache_increase(key,val):
    cache.incr(key,val)
    tmp = cache.get(key)
    #tmp = cache.get(key)
    #logger.debug("cache_set: {0} value before is {1}".format(key, tmp))
    #tmp = tmp + val
    #cache.set(key, tmp, 2*24*60*60)         #2天不过期
    #logger.debug("cache_set: {0} value after is {1}".format(key, tmp))
    return tmp