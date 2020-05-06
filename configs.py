#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 15:01
# @Author  : PoLoSec.
# @File    : configs.py
# @Software: PyCharm
import pymysql
from  flask import  Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test'
loginmanager=LoginManager()
loginmanager.login_view="login"
loginmanager.init_app(app)
db=SQLAlchemy()