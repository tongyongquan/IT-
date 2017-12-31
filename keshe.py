# encoding: utf-8
from datetime import timedelta
from flask import Flask, render_template, request, session, redirect, url_for, flash

import config
from models import *
from utils import create_md5

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

nav_select = {
    'main':                 u'主页',
    'content':              u'content',
    'article':              u'article',
    'big_web_knowledge':    u'大前端知识',
    'workplace':            u'挨踢职场',
    'community':            u'匿名社区',
    'login':                u'登录',
    'register':             u'注册',
}


def get_page_content():
    # type: () -> dict
    page_content = {
        'nav': nav_select['main'],
    }
    return page_content


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    page_content = get_page_content()
    page_content['nav'] = nav_select['login']
    if request.method == 'GET':
        return render_template('login.html', **page_content)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = create_md5(password)
        user = User.query.filter(User.username == username, User.password == password_hash).first()
        if user:
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=config.session_lifetime)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            page_content['error'] = u'用户名或密码错误!'
            return render_template('error.html', **page_content)


@app.route('/article/<article_id>/', methods=['GET', 'POST'])
def article(article_id):
    # user =User(username='tong',password='1111')
    # db.session.add(user)
    # db.session.commit()
    # label=Label(id='0',name='1',parent_id='1')
    # db.session.add(label)
    # db.session.commit()
    # article_add =Article(title='标题2',content='内容2',author_id='1',label_id='1')
    # db.session.add(article_add)
    # db.session.commit()
    article_model = Article.query.filter(Article.id == article_id).first()

    if request.method == 'GET':
        return render_template('article.html', article=article_model)
    else:
        pass


@app.route('/content', methods=['GET', 'POST'])
def content():
    if request.method == 'GET':
        return render_template('content.html')
    else:
        pass


if __name__ == '__main__':
    app.run()
