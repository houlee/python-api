# -*- coding: utf-8 -*-
from rotate import rotate,figureDegree
from ocr import ocr
import cv2


def showAndWaitKey1(winName, img):
    cv2.imshow(winName, img)
    cv2.waitKey()

if __name__ == '__main__':
    path = "./img/test11.jpg"
    #savepath = ["./img/test04r01.jpg","./img/test04r02.jpg","./img/test04r03.jpg","./img/test04r04.jpg"]
    #savepath = ["./img/test02r31.jpeg", "./img/test02r32.jpeg", "./img/test02r33.jpeg", "./img/test02r34.jpeg"]
    #savepath = ["./img/test05r01.jpg","./img/test05r02.jpg"]
    savepath = ["./img/test11r01.jpg"]
    precision = 2
    degree=figureDegree(path,precision)
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
    #单次旋转或两次
    for i in range(len(savepath)):
        rotateImg = rotate(path, degree[i])
        showAndWaitKey1("rotateImg", rotateImg)
        cv2.imwrite(savepath[i], rotateImg)
        ocr(savepath[i])

    cv2.destroyAllWindows()
