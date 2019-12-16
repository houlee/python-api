#!/usr/bin/python
# coding:utf-8
# 封装数据库操作
import pymysql
import mylog

logger = mylog.Logger(logname='mysqlpapi.log', loglevel=1, logger="hou").getlog()

class mysqlhou(object):
    __instance = None  # 定义一个类属性做判断
    __onetime = 0

    def __new__(cls, db_ip, db_user, db_pass, db_name):

        if cls.__instance == None:
            # 如果__instance为空证明是第一次创建实例
            # 通过父类的__new__(cls)创建实例
            cls.__instance = object.__new__(cls)

            return cls.__instance
        else:
            # 返回上一个对象的引用
            return cls.__instance


    #初始化
    def __init__(self, db_ip, db_user, db_pass, db_name):
        if self.__onetime == 0:
            self.__onetime+=1
            self.db_ip = db_ip
            self.db_user = db_user
            self.db_pass = db_pass
            self.db_name = db_name

        #self.logger.info("mysqlhou")

    # 获取数据库连接
    def getCon(self):
        try:
            conn = pymysql.connect(host=self.db_ip, user=self.db_user,password=self.db_pass,database=self.db_name,charset="utf8")
            return conn
        except Exception as e:
            logger.error("mysqlhou getCon Error:{0}".format(e))

    # 查询方法，
    def select(self, sql, *params):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql, params)
            fc = cur.fetchall()
            return fc
        except Exception as e:
            logger.error("mysqlhou select Error:{0}".format(e))
        finally:
            cur.close()
            con.close()

    # 更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')
    def update(self, sql, *params):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql, params)
            con.commit()
            return count
        except Exception as e:
            con.rollback()
            logger.error("mysqlhou update Error:{0}".format(e))
            return 0
        finally:
            cur.close()
            con.close()

# if __name__ =='__main__':
#     db_ip = '192.168.10.241'
#     db_user = 'root'
#     db_pass = 'stock123'
#     db_name = 'stockDB'
#
#     test=mysqlhou(db_ip,db_user,db_pass,db_name)
#
#     test.getCon()
#     sql = "SELECT MAX(id_basic) FROM stock_basic_info"
#     max = test.select(sql)
#     print(max)