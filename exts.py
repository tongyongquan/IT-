# encoding: utf-8

from flask_sqlalchemy import SQLAlchemy


class MySQLAlchemy(SQLAlchemy):
    def create_session(self, options):
        options['autoflush'] = False
        return super(MySQLAlchemy, self).create_session(options)


db = SQLAlchemy()
