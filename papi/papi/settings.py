"""
Django settings for papi project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR,'/app/python-api/papi/static/')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1rxoabyeto7@gh9(l+bwukv^*&=lm4-$y*z^lh^32oew@#d5#r'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'django_crontab',
    'imgRotate',  # 添加imgRotate app
    'rest_framework',  # 添加rest_framework
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'papi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'papi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', #固定配置
#        'HOST': '192.168.10.241',#mysql地址
#        'PORT': '3306',#端口号
#        'NAME': 'BLOGDB',#库名（组名）
#        'USER': 'root',#用户
#        'PASSWORD': 'password',#密码
#        'OPTIONS': {'init_command': "SET sql_mode='traditional'", },
#    }
}

#django CACHE
CACHES = {
'default': {
'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
'LOCATION': 'papi-var-cache'
}
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#增加一段REST_FRAMEWORK配置
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

#日志配置
cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'log')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
#格式 描述%(name)s 记录器的名称 %(levelno)s 数字形式的日志记录级别 %(levelname)s 日志记录级别的文本名称 %(filename)s 执行日志记录调用的源文件的文件名称
#%(pathname)s 执行日志记录调用的源文件的路径名称 %(funcName)s 执行日志记录调用的函数名称 %(module)s 执行日志记录调用的模块名称 %(lineno)s 执行日志记录调用的行号 %(created)s 执行日志记录的时间
#%(asctime)s 日期和时间 %(msecs)s 毫秒部分 %(thread)d 线程ID %(threadName)s 线程名称 %(process)d 进程ID %(message)s 记录的消息
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(process)d]'
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            #'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 按时间切割日志
            #'filename': os.path.join(log_path, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'filename': os.path.join(log_path, 'all.log'),
            #'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },

        #注释掉info日志
        # 输出info日志
        #'info': {
        #    'level': 'INFO',
        #    'class': 'logging.handlers.RotatingFileHandler',
        #    'filename': os.path.join(log_path, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
        #    'maxBytes': 1024 * 1024 * 5,
        #    'backupCount': 5,
        #    'formatter': 'standard',
        #    'encoding': 'utf-8',  # 设置默认编码
        #},

    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'console', 'default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}


'''
CRONJOBS = [
    # 每天0：05执行
    #('05 0 * * *', 'imgRotate.job.reset_data', '>>/Users/houlee/Documents/git_dev/python-api/papi/log/xxx.log')
    # 每分钟执行
    ('*/1 * * * *', 'imgRotate.job.resetData', '>>/Users/houlee/Documents/git_dev/python-api/papi/log/xxx.log')
 ]

 第一个参数（表示时间）：
 前5个字段分别表示：
 	• 分钟：0-59
 	• 小时：1-23
 	• 日期：1-31
 	• 月份：1-12
 	• 星期：0-6（0表示周日）
 一些特殊符号：
 *： 表示任何时刻
 ,：　表示分割
 -：表示一个段，如第二端里： 1-5，就表示1到5点
 /n : 表示每个n的单位执行一次，如第二段里，*/1, 就表示每隔1个小时执行一次命令。也可以写成1-23/1.
 第二个参数（表示路径）：
 格式：app名称/文件名/函数名
 如果想生成日志，那就再加一个字符串类型的参数：'>> path/name.log'， path路径，name文件名。'>>'表示追加写入，'>'表示覆盖写入。
 提示：如果你有多个定时任务，以逗号隔开，都放入CORJOBS中即可。
'''

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
