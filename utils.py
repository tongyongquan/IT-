# encoding: utf-8

from hashlib import md5
import config


# 获取原始密码+salt的md5值
def create_md5(pwd):
    md5_obj = md5()
    md5_obj.update(pwd + config.SALT)
    return md5_obj.hexdigest()
