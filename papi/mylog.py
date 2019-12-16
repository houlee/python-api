#!/usr/bin/python
# coding:utf-8
# 封装日志操作
import logging
from logging.handlers import TimedRotatingFileHandler

#单例模式
# def singleton(cls, *args, **kw):
#     instances = {}
#     def _singleton():
#         if cls not in instances:
#             instances[cls] = cls(*args, **kw)
#         return instances[cls]
#     return _singleton
# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
#@singleton
class Logger(object):
    __instance = None  # 定义一个类属性做判断
    __onetime = 0

    def __new__(cls, logname, loglevel, logger):

        if cls.__instance == None:
            # 如果__instance为空证明是第一次创建实例
            # 通过父类的__new__(cls)创建实例
            cls.__instance = object.__new__(cls)

            return cls.__instance
        else:
            # 返回上一个对象的引用
            return cls.__instance

    def __init__(self, logname, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        print(logname)
        if self.__onetime == 0:
            print(logname)
            self.__onetime=+1
            # 用字典保存日志级别
            format_dict = {
                1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            }
            # 创建一个logger
            self.logger = logging.getLogger(logger)
            self.logger.setLevel(logging.DEBUG)

            # 创建一个handler，用于写入日志文件
            #fh = logging.FileHandler(logname)
            fh = TimedRotatingFileHandler(logname, when="midnight", interval=1, backupCount=1, encoding='utf-8')
            fh.suffix = "%Y-%m-%d"
            fh.setLevel(logging.DEBUG)

            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # 定义handler的输出格式
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter = format_dict[int(loglevel)]
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

#用法
#import mylog
#logger = mylog.Logger(logname='log.txt', loglevel=1, logger="fox").getlog()
#logger.info("test")