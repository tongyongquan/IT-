# encoding: utf-8
import sys
from datetime import timedelta

from flask import Flask, render_template, session, redirect, url_for, make_response, g
from sqlalchemy import func

from decorators import login_required, article_author_required, admin_required
from services import *
from utils import create_md5

reload(sys)
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
app.config.from_object(config)
# jinja extension 添加表达式的语句支持  do loop(for)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db.init_app(app)
# 添加jinja的全局变量 session
app.jinja_env.globals['session'] = session
app.jinja_env.globals['db'] = db
app.jinja_env.globals['User'] = User
app.jinja_env.auto_reload = True


@app.before_request
def before_request():
    user_id = session.get('user_id')
    g.user = None
    if user_id:
        session_user = User.query.filter(User.id == user_id).first()
        if session_user:
            g.user = session_user


@app.route('/')
def index():
    page_content = get_page_content()
    # 右边
    # 栏目列表
    set_column_list(page_content)
    # 推荐内容
    set_recommended_content(page_content)
    # 热点内容
    set_hot_content(page_content)
    # 最新更新
    index_article = Article.query.filter().order_by(Article.modify_time).offset(0).limit(14).all()
    index_article = map(to_article_info, index_article)
    page_content['index_article'] = index_article

    # 特别推荐
    good_article_list = Article.query.filter().order_by(
        Article.good_count.desc(), Article.modify_time.desc()
    ).offset(0).limit(8).all()
    page_content['good_article_list'] = map(article_modify_time_to_month_day, good_article_list)
    # 最下面的栏目
    nav_label = page_content['nav_label']
    label_main_article_dict = {}
    for label in nav_label:
        article_list = Article.query.filter(Article.label_id == label.id).order_by(
            Article.click_count.desc(), Article.modify_time.desc()
        ).offset(0).limit(8).all()
        label_main_article_dict[label.id] = map(article_modify_time_to_month_day, article_list)
    page_content['label_main_article_dict'] = label_main_article_dict
    return render_template('index.html', **page_content)


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
        login_user = User.query.filter(User.username == username, User.password == password_hash).first()
        if login_user:
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=config.session_lifetime)
            session['user_id'] = login_user.id
            user_authority = UserAuthority.query.filter(UserAuthority.user == login_user).first()
            if user_authority:
                session['admin_id'] = login_user.id
            return redirect(url_for('index'))
        else:
            page_content['error'] = u'用户名或密码错误!'
            return render_template('error.html', **page_content)


@app.route('/captcha')
def get_verify_code():
    # 把strs发给前端,或者在后台使用session保存
    # code_img, code_text = utils.generate_verification_code()
    # captcha = object

    code_img, code_text = captcha.generate_verification_code()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=config.captcha_time)
    session['code_text'] = code_text.lower()
    print session['code_text']
    response = make_response(code_img)
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Pragma'] = 'No-cache'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Cache-Expires'] = -10
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    page_content = get_page_content()
    page_content['nav'] = nav_select['register']
    if request.method == 'GET':
        return render_template('register.html', **page_content)
    else:
        captcha_text = session.get('code_text')
        page_content['error'] = u'验证码错误!'
        if captcha_text is None:
            return render_template('error.html', **page_content)
        else:
            captcha_form = request.form.get('captcha')
            if captcha_text != str(captcha_form).lower():
                return render_template('error.html', **page_content)
            username = request.form.get('username')
            password = request.form.get('password')
            if username == '' or password == '':
                page_content['error'] = u'用户名或密码为空!'
                return render_template('error.html', **page_content)
            re_password = request.form.get('re_password')
            if password != re_password:
                page_content['error'] = u'两次密码不一致!'
                return render_template('error.html', **page_content)
            # avatar = request.form.get('avatar')
            register_user = User.query.filter(User.username == username).first()
            if register_user:
                page_content['error'] = u'用户已存在!'
                return render_template('error.html', **page_content)
            register_user = User(username=username, password=create_md5(password))
            del page_content['error']
            db.session.add(register_user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/article/<article_id>', methods=['GET', 'POST'])
def article(article_id):
    page_content = get_page_content()
    article_model = Article.query.filter(Article.id == article_id).first()
    if not article_model:
        page_content['error'] = u'文章不存在!'
        return render_template('error.html', **page_content)
    page_content['article'] = article_model
    page_content['content'] = article_model.content
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('size', config.page_size, type=int)
    comment_paginate = Comment.query.filter(Comment.article_id == article_id) \
        .order_by(Comment.create_time.desc()).paginate(page, page_size)
    page_content['comment_paginate'] = comment_paginate

    # 网页的地址
    page_content['base_url'] = get_base_url()
    # 内容最上面的路径导航
    path_label = get_path_label(article_model.label)
    page_content['path_label'] = path_label

    # 激活选项
    page_content['nav'] = path_label[0].name
    # 右边
    # 栏目列表
    set_column_list(page_content)
    # 推荐内容
    set_recommended_content(page_content)
    # 热点内容
    set_hot_content(page_content)
    if not article_model:
        page_content['error'] = u'这篇文章不存在'
        return render_template('error.html', **page_content)
    if request.method == 'GET':
        return render_template('article.html', **page_content)
    else:
        pass


@app.route('/user', methods=['POST', 'GET'])
@login_required
def user_login():
    page_content = get_page_content()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('size', config.page_size, type=int)
    label_id = request.args.get('label_id', None, type=int)
    if not label_id:
        article_pagination = Article.query.filter(Article.author_id == g.user.id).order_by(
            Article.modify_time.desc()).paginate(
            page=page, per_page=page_size)
    else:
        article_pagination = Article.query.filter(Article.author_id == g.user.id,
                                                  Article.label_id == label_id).order_by(
            Article.modify_time.desc()).paginate(
            page=page, per_page=page_size)
    # 分页
    page_content['article_pagination'] = article_pagination
    # 网页的地址
    page_content['base_url'] = get_base_url()

    article_id_list = model_list_to_id_list(article_pagination.items)
    article_comment_count_list = db.session.query(Comment.article_id, func.count(1)).filter(
        Comment.article_id.in_(article_id_list)).group_by(
        Comment.article_id).all()
    article_comment_count_dict = get_article_comment_count_dict(article_comment_count_list)
    page_content['article_comment_count_dict'] = article_comment_count_dict
    page_content['user'] = g.user
    return render_template('user.html', **page_content)


@app.route('/article/add', methods=['POST', 'GET'])
@login_required
def article_add():
    if request.method == 'GET':
        page_content = get_page_content()
        all_label = Label.query.all()
        page_content['all_label'] = all_label
        return render_template('article/add.html', **page_content)
    else:
        title = request.form.get('title')
        info = request.form.get('info')
        label_id = request.form.get('label_id')
        form_content = request.form.get('content')
        user = g.user
        article_model = Article(title=title, info=info, content=form_content, label_id=label_id)
        article_model.author = user
        db.session.add(article_model)
        db.session.commit()
        return redirect(url_for('user_login'))


@app.route('/article/delete/<article_id>', methods=['POST', 'GET'])
@login_required
@article_author_required
def article_delete(article_id):
    article_model = Article.query.filter(Article.id == article_id).first()
    if request.method == 'GET':
        # 删除文章
        Comment.query.filter(Comment.article == article_model).delete(synchronize_session=False)
        db.session.delete(article_model)
        db.session.commit()
    return redirect(url_for('user_login'))


@app.route('/article/edit/<article_id>', methods=['POST', 'GET'])
@login_required
@article_author_required
def article_edit(article_id):
    page_content = get_page_content()
    article_model = Article.query.filter(Article.id == article_id).first()
    if request.method == 'GET':
        page_content['article'] = article_model
        all_label = Label.query.all()
        page_content['all_label'] = all_label
        return render_template('article/edit.html', **page_content)
    else:
        title = request.form.get('title')
        info = request.form.get('info')
        label_id = request.form.get('label_id')
        form_content = request.form.get('content')
        article_model.title = title
        article_model.info = info
        article_model.content = form_content
        article_model.label_id = label_id
        article_model.modify_time = datetime.now()
        db.session.commit()
        return redirect(url_for('user_login'))


@app.route('/comment/add/<article_id>', methods=['GET', 'POST'])
@login_required
def add_comment(article_id):
    article_model = Article.query.filter(Article.id == article_id).first()
    if request.method == 'POST':
        user_id = session.get('user_id')
        comment_content = request.form.get('comment_content')
        comment = Comment(content=comment_content, user_id=user_id)
        user_model = User.query.filter(User.id == user_id).first()
        comment.user = user_model
        comment.article = article_model
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article', article_id=article_id))
    else:
        pass


@app.route('/content_main')
def content_main():
    return redirect(url_for('content', label_id=0))


@app.route('/content/<label_id>')
def content(label_id=0):
    page_content = get_page_content()

    # 父标签和自己

    # 是否是没有标签的页
    is_main = str(label_id) == str(0)
    current_label = None
    if is_main:
        label_list = Label.query.all()
    else:
        current_label = Label.query.filter(Label.id == label_id).first()
        label = current_label
        if label is None:
            page_content['error'] = u'标签不存在'
            return render_template('error.html', **page_content)
        label_list = get_path_label(label)
    # 内容最上面的路径导航
    page_content['path_label'] = label_list

    # 网页的地址
    page_content['base_url'] = get_base_url()

    # 分页
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('size', config.page_size, type=int)
    if not is_main:
        # 设置导航栏的激活状态
        page_content['nav'] = label_list[0].name
        label_list_new = Label.query.filter(Label.parent_id == current_label.id).all()
        label_list_new.insert(0, current_label)
        label_list = label_list_new
    label_id_list = map(lambda label_lam: label_lam.id, label_list)
    article_pagination = Article.query.filter(
        Article.label_id.in_(label_id_list)).order_by(
        Article.modify_time.desc()).paginate(
        page=page, per_page=page_size)
    db.session.close()
    article_pagination.items = map(to_article_info, article_pagination.items)
    page_content['article_pagination'] = article_pagination

    # 右边
    # 栏目列表
    set_column_list(page_content)
    # 推荐内容
    set_recommended_content(page_content)
    # 热点内容
    set_hot_content(page_content)

    return render_template('content.html', **page_content)


@app.route('/admin')
@login_required
@admin_required
def admin():
    all_label = Label.query.all()
    page_content = get_page_content()
    page_content['nav'] = nav_select['label']
    page_content['all_label'] = all_label

    return render_template('admin/index.html', **page_content)


@app.route('/label/edit/<label_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def label_edit(label_id):
    page_content = get_page_content()
    page_content['nav'] = nav_select['label']
    label = Label.query.filter(Label.id == label_id).first()

    if not label:
        page_content['error'] = u'标签不存在!'
        return render_template('error.html', **page_content)
    page_content['label'] = label
    if request.method == 'GET':
        all_label = Label.query.filter(Label.id != label_id).all()
        page_content['all_label'] = all_label
        return render_template('label/edit.html', **page_content)
    else:
        name = request.form.get('name')
        if name == '':
            page_content['error'] = u'标签名不能为空!'
            return render_template('error.html', **page_content)
        temp = Label.query.filter(Label.name == name).first()
        if temp and temp != label:
            page_content['error'] = u'已经存在该标签名!'
            return render_template('error.html', **page_content)
        parent_id = request.form.get('parent_id')
        label.name = name
        parent = Label.query.filter(Label.id == parent_id).first()
        label.parent = parent
        db.session.commit()
        return redirect(url_for('admin'))


@app.route('/label/add', methods=['GET', 'POST'])
@login_required
@admin_required
def label_add():
    page_content = get_page_content()
    page_content['nav'] = nav_select['label']
    if request.method == 'GET':
        all_label = Label.query.all()
        page_content['all_label'] = all_label
        return render_template('label/add.html', **page_content)
    else:
        name = request.form.get('name')
        if name == '':
            page_content['error'] = u'标签名不能为空!'
            return render_template('error.html', **page_content)
        temp = Label.query.filter(Label.name == name).first()
        if temp:
            page_content['error'] = u'已经存在该标签名!'
            return render_template('error.html', **page_content)
        parent_id = request.form.get('parent_id')
        parent = Label.query.filter(Label.id == parent_id).first()
        label = Label(name=name)
        label.parent = parent
        db.session.add(label)
        db.session.commit()
        return redirect(url_for('admin'))


@app.route('/label/delete/<label_id>')
@login_required
@admin_required
def label_delete(label_id):
    label = Label.query.filter(Label.id == label_id).first()
    if label:
        children_label = Label.query.filter(Label.parent_id == label_id).all()
        other_label = Label.query.filter(Label.name == '其他').first()
        for child in children_label:
            child.parent = other_label
        db.session.delete(label)
        db.session.commit()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(port=8888)
