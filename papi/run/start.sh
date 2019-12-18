#!/bin/bash

#启动虚拟环境
#cd /app/python-api
#pipenv shell
#sleep 1

#先手动进入虚拟环境
#停止服务器
cd /app/python-api/papi/
uwsgi --stop run/uwsgi.pid

#启动服务器
uwsgi --ini uwsgi.ini

#重启服务器
uwsgi --reload run/uwsgi.pid
