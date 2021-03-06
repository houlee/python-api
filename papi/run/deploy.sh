#!/bin/bash

#启动虚拟环境
#cd /app/python-api
#pipenv shell
#sleep 1

#先手动进入虚拟环境
#停止服务器
#cd /app/python-api/papi/
#uwsgi --stop run/uwsgi.pid

#备份代码
cd /app/
cp -rf python-api python-api-backup
sleep 2

#同步代码
cd /app/python-api/papi
git fetch --all;
git reset --hard origin/master;
sleep 2

#重启服务器
uwsgi --reload run/uwsgi.pid

#赋予脚本执行权限
cd /app/python-api/papi/run
chmod +x *.sh