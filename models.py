#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 15:00
# @Author  : PoLoSec.
# @File    : models.py
# @Software: PyCharm
from configs import  db
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20))
    status=db.Column(db.Integer,default=0)
    def __init__(self,u,p,e,s): ##初始化的时候传进来0 默认普通用户
        self.username=u
        self.password=p
        self.email=e
        self.status=s
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return True
    def get_id(self):
        return unicode(self.id)
    def __repr__(self):
        return 'user %s' %self.username
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    isbn=db.Column(db.String(50))
    name = db.Column(db.String(16), unique=True)
    price =db.Column(db.Float,default=0)
    num=db.Column(db.Integer,default=1)
    author=db.Column(db.String(20))
    status=db.Column(db.Integer,default=1)
    def __repr__(self):
        return 'Book: %s %s' % (self.name, self.author_id)
    def __init__(self,isbn,name,price,author,num):
        self.isbn=isbn
        self.name=name
        self.price=price
        self.author=author
        self.num=num