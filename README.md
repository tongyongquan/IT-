# 课程设计
基于python2.7的flask的web开发框架的课程设计

## mysql脚本:
    '''
    grant all privileges on *.* to 'user'@'%' identified by 'happy100';
    flush privileges;
    CREATE DATABASE ke_she charset utf8;
    '''

#如果要安装requirements.txt中的类库内容，那么你可以执行pip install -r requirements.txt.

#初始化SQLAlchemy版本库 python manage.py db init
#生成迁移文件  python manage.py db migrate
#映射到数据库  python manage.py db upgrade

#2018-1-04