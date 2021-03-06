from django.conf import settings

#控制测试环境的全局变量
global g_debug
g_debug = settings.DEBUG

#用全局变量定义使用的ocr type，1 BDOCR; 2 FKOCR
#使用全局变量控制OCR类型，和传入参数无关，默认使用BDOCR，在BDOCR次数用尽后，使用FKOCR，每天零点，重置为1
global g_ocr_type
g_ocr_type = 1

#计数百度OCR调用次数，重启或零点重置为0
global g_count_bdocr
g_count_bdocr = 0
