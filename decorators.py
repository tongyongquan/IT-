# encoding: utf-8

from functools import wraps

from flask import redirect, url_for, g, render_template, session

# 登录限制的装饰器
from models import Article, UserAuthority


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper


def article_author_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        article_model = Article.query.filter(Article.id == kwargs['article_id']).first()
        if not article_model:
            return render_template('error.html', error=u'这篇文章不存在!')
        if article_model.author != g.user:
            return render_template('error.html', error=u'你没有权限操作这篇文章!')
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        admin_id = session.get('admin_id')
        if not admin_id:
            return render_template('error.html', error=u'你没有权限访问!')
        return func(*args, **kwargs)

    return wrapper
