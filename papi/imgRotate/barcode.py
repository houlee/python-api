# -*- coding: utf-8 -*-
#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from . import utils
import cv2
#from imgRotate import logger
import pyzbar.pyzbar as pyzbar
#日志设置
import logging
logger = logging.getLogger('log')

def barcode_detect(image_path):
    # 判断是否网络图片还是本地图片
    if image_path.find('http') != -1:  # 网络图片
        # print("network pic")
        # 读取图片，灰度化
        gray = utils.url_to_image(image_path, cv2.IMREAD_GRAYSCALE)
        # showAndWaitKey("gray", gray)
    else:  # 本地图片
        # print("local pic")
        # 读取图片，灰度化
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # showAndWaitKey("gray", gray)
    barcodes = pyzbar.decode(gray)
    if barcodes != []:
        logger.info('barcode:{0}'.format(barcodes))
        return 1

    #for barcode in barcodes:
    #    barcodeData = barcode.data.decode("utf-8")
    #    print(barcodeData)


'''
if __name__ == '__main__':
    img = "img/ewm010.jpg"
    barcode_detect(img)
'''