# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pymysql
pymysql.install_as_MySQLdb()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test'
db = SQLAlchemy(app)
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
class BookForm(FlaskForm):
    name = StringField('书籍名称', validators=[DataRequired()])
    isbn=StringField('ISBN号',validators=[DataRequired()])
    price=StringField('价格',validators=[DataRequired()])
    author=StringField('作者',validators=[DataRequired()])
    submit = SubmitField('提交')

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)#返回实体：一条记录
    try:
            book.status=0
            db.session.commit()
            flash('删除图书成功')
    except Exception as e:
            print(e)
            flash('删除书籍失败')
            db.session.rollback()

    return redirect(url_for('showallbooks'))
@app.route('/showallbooks', methods=['GET', 'POST'])
def showallbooks():
    books = Book.query.all()
    return render_template('show_books.html', books=books)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')
@app.route('/addbook',methods=['GET','POST'])
def addbook():
    bookform=BookForm()
    if request.method=="POST":
        isbn=request.form.get('isbn')
        name=request.form.get('name')
        price=request.form.get('price')
        author=request.form.get('author')
        book=Book(isbn=isbn,price=price,name=name,author=author,num=1)
        if bookform.validate_on_submit():
            try:
                db.session.add(book)
                db.session.commit()
                flash('添加图书成功')
            except Exception as e:
                flash('添加书籍失败')
            return redirect(url_for('showallbooks'))
    return  render_template('addbook.html',bookform=bookform)
if __name__ == '__main__':
    app.run(debug=True)
