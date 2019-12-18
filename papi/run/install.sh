#!/bin/bash

#安装 pipenv 并设置环境变量
pip install --user pipenv;
sleep 5;
pip install --user virtualenv;
sleep 5;
cat <<EOF >>~/.bashrc
export PATH=\$PATH:/opt/server/python3.7/bin
EOF
source ~/.bashrc;
sleep 1;
#clone代码
cd /app/;
git clone https://github.com/houlee/python-api;
sleep 10;
#安装pipenv环境
cd /app/python-api/;
pipenv --python /opt/server/python3.7/bin/python3.7;
sleep 10;
#建目录
cd /app/python-api/papi;
mkdir image_temp;
mkdir run;
mkdir log;
#安装pipfile.lock中的包
cd /app/python-api/;
pipenv install;