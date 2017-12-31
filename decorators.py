# encoding: utf-8

from functools import wraps

from flask import redirect, url_for, g


# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
