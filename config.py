# encoding: utf-8
import os

DEBUG = True
SECRET_KEY = os.urandom(4)

DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'user'
PASSWORD = 'happy100'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'ke_she'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SALT = 'huangdy8745tongyongquan'

# 用户session的过期时间 天
session_lifetime = 5

# 验证码列型   0 英文   1 中文
captcha_type = 0

# 验证码过期时间 分钟
captcha_time = 2

# 不使用 csrf
WTF_CSRF_ENABLED = False

# 一页的条数
page_size = 10

# 推荐内容的简介的长度
article_introduction_length = 45


