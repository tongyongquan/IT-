# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=1, max=100)])
    password = StringField("password", validators=[DataRequired(), Length(min=1, max=100)])


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=1, max=100)])
    password = StringField("password", validators=[DataRequired(), Length(min=1, max=100)])
    captcha = StringField("captcha", validators=[DataRequired()])
