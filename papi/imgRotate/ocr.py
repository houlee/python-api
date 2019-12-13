# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image
#pip install pytesseract，pip install tesseract，pip install tesseract-ocr，
#必须要能识别出线条，否则会报错


def ocr(path):
    # image = Image.open("./img/test04r01.jpg")
    image = Image.open(path)
    # 对图片进行阈值过滤（低于143的置为黑色，否则为白色）
    # 相当于对电脑显卡调节对比度(电脑显卡对比度默认为50,我比较习惯于调成53)
    image = image.point(lambda x: 0 if x < 143 else 255)
    # 重新保存图片
    image.save(path)
    code = pytesseract.image_to_string(image, lang='chi_sim')
    print(code)
    return code


