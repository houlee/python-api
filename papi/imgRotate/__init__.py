import mylog
import os

logger = mylog.Logger(logname='./log/imgRotate.log', loglevel=1, logger="imgRotate-app").getlog()
logger.info("project starting ...")
val=os.popen('pwd').read()
logger.info('project path:{0}'.format(val))
