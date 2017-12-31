# encoding: utf-8
import os

DEBUG = True
SECRET_KEY = os.urandom(24)

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
