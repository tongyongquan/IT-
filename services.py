# encoding: utf-8


# 导航条文本
from flask import request

import captcha_cn
import captcha_en
import config
from models import *

nav_select = {
    'main': u'主页',
    'content': u'content',
    'article': u'article',
    'big_web_knowledge': u'大前端知识',
    'workplace': u'挨踢职场',
    'community': u'匿名社区',
    'login': u'登录',
    'register': u'注册',
    'user': u'个人中心',
    'logout': u'注销',
}


# 网页模板的返回参数 统一
def get_page_content():
    # type: () -> dict
    page_content = {
        'nav': nav_select['main'],
    }
    # 设置导航栏标签的选项
    to_nav_label(page_content)
    return page_content


# nav 设置导航栏的选项
def to_nav_label(page_content):
    nav_label = Label.query.filter(Label.parent_id.is_(None)).all()
    page_content['nav_label'] = nav_label


# 定义栏目列表
def set_column_list(page_content):
    label_list = Label.query.all()
    page_content['column_label_list'] = label_list


# 设置推荐内容
def set_recommended_content(page_content):
    recommended_content = Article.query.filter().order_by(
        Article.good_count.desc(), Article.modify_time.desc()).offset(0).limit(6).all()
    recommended_content = map(to_article_info, recommended_content)
    page_content['recommended_content'] = recommended_content


# 获取标签路径导航
def get_path_label(label):
    label_list = []
    label_list.insert(0, label)
    while label.parent:
        label = label.parent
        label_list.insert(0, label)
    return label_list


# 文章转简要介绍
def to_article_info(article):
    # article2 -> Article
    info = article.info
    if len(article.info) > config.article_introduction_length:
        info = article.info[0:config.article_introduction_length - 3] + '...'
    article_temp = Article(id=article.id, title=article.title, info=info)
    return article_temp


# 设置热点内容
def set_hot_content(page_content):
    hot_content = Article.query.filter().order_by(
        Article.click_count.desc(), Article.modify_time.desc()).offset(0).limit(10).all()
    hot_content = map(to_article_for_hot_content, hot_content)
    page_content['hot_content'] = hot_content


#  只要文章的标题和id
def to_article_for_hot_content(article2):
    # article2 -> Article
    article_temp = Article(id=article2.id, title=article2.title)
    return article_temp


# 获取对象的id 针对数据库模型对象
def model_list_to_id_list(model_list):
    return map(lambda model: model.id, model_list)


# 评论文章的元祖转成字典
def get_article_comment_count_dict(article_comment_count_list):
    article_comment_count_dict = {}
    for article_id, comment_count in article_comment_count_list:
        article_comment_count_dict[article_id] = comment_count
    return article_comment_count_dict


# 获取请求的除了host的后面路径
def get_base_url():
    return request.base_url[len(request.url_root) - 1:]


if config.captcha_type == 0:
    captcha = captcha_en
else:
    captcha = captcha_cn


# 日期转 月日
def get_month_day(date):
    """
    :type date: datetime
    :param date: datetime
    :return: date_str
    """
    return date.strftime("%m-%d")


def article_modify_time_to_month_day(article):
    """
        :type article: Article
        :param article: Article
        :return: Article
    """
    article_temp = Article(id=article.id, title=article.title, modify_time=get_month_day(article.modify_time),
                           create_time=get_month_day(article.create_time), info=article.info)
    return article_temp
