import mylog
import os
from apscheduler.schedulers.background import BackgroundScheduler
from .global_data import g_ocr_type,g_count_bdocr

#日志初始化
logger = mylog.Logger(logname='./log/imgRotate.log', loglevel=1, logger="imgRotate-app").getlog()
logger.info("project starting ...")
val=os.popen('pwd').read()
logger.info('project path:{0}'.format(val))

#job

#用全局变量定义使用的ocr type，1 BDOCR; 2 FKOCR
#使用全局变量控制OCR类型，和传入参数无关，默认使用BDOCR，在BDOCR次数用尽后，使用FKOCR，每天零点，重置为1
#g_ocr_type=1
#计数百度OCR调用次数，重启或零点重置为0
#g_count_bdocr = 0

def job_resetData():
    global g_ocr_type
    global g_count_bdocr
    logger.info("*** job resetData *** ")
    logger.info("*** job resetData before *** g_ocr_type={0}, g_count_bdocr={1}".format(g_ocr_type,g_count_bdocr))
    g_ocr_type = 1
    g_count_bdocr = 0
    #os.popen("touch /Users/houlee/Documents/git_dev/python-api/papi/1.txt")
    logger.info("*** job resetData after *** g_ocr_type={0}, g_count_bdocr={1}".format(g_ocr_type,g_count_bdocr))
    logger.info("*** job resetData *** ")

# BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用
scheduler = BackgroundScheduler()
# 采用阻塞的方式

# 采用cron的方式
#scheduler.add_job(job_resetData, 'cron', second='*/5')
#每天0:05执行
scheduler.add_job(job_resetData, 'cron', hour='0',minute='5',day='*/1')
scheduler.start()

'''
year (int|str) – 4-digit year
month (int|str) – month (1-12)
day (int|str) – day of the (1-31)
week (int|str) – ISO week (1-53)
day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
hour (int|str) – hour (0-23)
minute (int|str) – minute (0-59)
second (int|str) – second (0-59)

start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)

*    any    Fire on every value
*/a    any    Fire every a values, starting from the minimum
a-b    any    Fire on any value within the a-b range (a must be smaller than b)
a-b/c    any    Fire every c values within the a-b range
xth y    day    Fire on the x -th occurrence of weekday y within the month
last x    day    Fire on the last occurrence of weekday x within the month
last    day    Fire on the last day within the month
x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
'''



