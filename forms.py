#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 14:59
# @Author  : PoLoSec.
# @File    : forms.py
# @Software: PyCharm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FileField
from wtforms.validators import DataRequired,EqualTo
class BookForm(FlaskForm):
    name = StringField('书籍名称', validators=[DataRequired()])
    isbn=StringField('ISBN号',validators=[DataRequired()])
    price=StringField('价格',validators=[DataRequired()])
    author=StringField('作者',validators=[DataRequired()])
    submit = SubmitField('提交')
class LoginForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired()])
    password=StringField('密码',validators=[DataRequired()])
    submit=SubmitField('提交',validators=[DataRequired()])
class RegisterForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired()])
    password=StringField('密码',validators=[DataRequired()])
    password_conf=StringField('确认密码',validators=[DataRequired()])
    email=StringField('邮箱',validators=[DataRequired()])
    submit=SubmitField('提交',validators=[DataRequired()])
class FindBookForm(FlaskForm):
    name=StringField('书名')
    isbn=StringField('isbn')
    submit=SubmitField('提交')
class ForgotForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired()])
    email=StringField('邮箱',validators=[DataRequired()])
    password = StringField('新密码', validators=[DataRequired()])
    password_conf = StringField('确认密码', validators=[DataRequired(),EqualTo('password','两次密码不一致')])
    submit=SubmitField('提交')
class UploadForm(FlaskForm):
    file=FileField('文件名')
    submit=SubmitField('提交')
class ModForm(FlaskForm):
    email=StringField('邮箱',validators=[DataRequired()])
    email_conf=StringField('确认邮箱',validators=[DataRequired(),EqualTo('email')])

    submit=SubmitField('提交')
class ChangepwdForm(FlaskForm):
    password=StringField('新密码',validators=[DataRequired()])
    password_conf=StringField('确认密码',validators=[DataRequired()])
    submit=SubmitField('提交')
