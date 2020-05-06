# -*- coding: utf-8 -*-
from configs import db,loginmanager,app
from models import Book,User
from forms import RegisterForm,LoginForm,BookForm,FindBookForm,ForgotForm,UploadForm,ModForm
from flask import Flask, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, login_required,logout_user,current_user
import sys,os
reload(sys)
upload_dir='C:\\Users\\69027\\Desktop\\bms\\upload'
sys.setdefaultencoding('utf-8')
db.init_app(app) #type:Flask
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
    session['username']='test'
    return render_template('index.html')
@app.route('/addbook',methods=['GET','POST'])
@login_required
def addbook():
    if current_user.status ==1:
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
    else :return ' permission denied'
@loginmanager.user_loader
def load_user(userid):
    return User.query.get(int(userid))
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/login',methods=['GET','POST'])
def login():
    loginform=LoginForm()
    if request.method=='POST':
        if(loginform.validate_on_submit()):
            username=request.form.get('username')
            password=request.form.get('password')
            user=User.query.filter(User.username==username,User.password==password).first()
            if(user):
                login_user(user)
                return render_template('profile.html')
    return  render_template('login.html',loginform=loginform)
@app.route('/register',methods=['GET','POST'])
def register():
    regform=RegisterForm()
    if request.method=='POST':
        if(regform.validate_on_submit()):
            username = request.form.get('username')
            password = request.form.get('password')
            email=request.form.get('email')
            user=User(username,password,email,0)
            db.session.add(user)
            db.session.commit()
            return  'reg success'
        else : return 'fail'
    return  render_template('register.html',regform=regform)
@app.route('/findbook',methods=['GET','POST'])
def findbook():
    bookform=FindBookForm()
    if request.method=="POST":
        isbn=request.form.get('isbn')
        name=request.form.get('name')
        if isbn=="" and name!= "":
            books=Book.query.filter(Book.name.like('%'+name+'%')).all()
            return render_template('findbook.html',books=books,form=bookform)
        elif name=="" and isbn!="":
            books = Book.query.filter(Book.isbn == isbn).all()
            return render_template('findbook.html',books=books,form=bookform)
        elif name!="" and isbn!="":
            books = Book.query.filter(Book.isbn == isbn).all()
            return render_template('findbook.html', books=books,form=bookform)
        else :
            flash('请输入ISBN号或者书名进行查询！')

        return  render_template('findbook.html',form=bookform,books="")
    return render_template('findbook.html',form=bookform,books="")
@app.route('/borrowbook')
def borrowbook():
    pass
@app.route('/returnbook')
def returnbook():
    # if(session.get('username') is None): 测试session用法
    #     return 'loginfirst'
    # else :return 'sussess'
    pass
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    forgotForm=ForgotForm()
    if request.method=="POST":
        if forgotForm.validate_on_submit():
            username=request.form.get('username')
            password=request.form.get('password')#下一步用hash加密
            email=request.form.get('email')
            user=User.query.filter(User.username==username,User.email==email).first()
            if user:
                user.password=password
                db.session.commit()
                flash('用户密码已重置！')
                return render_template('forgot.html',form=forgotForm)

    return render_template('forgot.html',form=forgotForm)
@app.route('/uploadfile',methods=['GET','POST'])
@login_required
def upload():
    # uploadform=UploadForm()
    # if request.method=="POST":
    #     if uploadform.validate_on_submit():
    #         file=request.files['file']
    #         file.save(os.path.join(upload_dir,file.filename))
    #         if(file.filename==""):
    #             filename="default.jpg"
    #         else:    filename=file.filename
    #         user=User.query.filter(User.username==current_user.username).first()
    #         if user:
    #             user.filename=filename
    #             url = os.path.join(upload_dir, user.filename)
    #             db.session.commit()
    #             return render_template('profile.html',url=url)
    # return render_template('upload.html',form=uploadform)
    pass
@app.route('/modify',methods=['POST','GET'])
@login_required
def modify():
    modform=ModForm()
    cu=current_user.username
    if request.method=="POST":
        if(modform.validate_on_submit()):
            email=request.form.get('email')
            user=User.query.filter(User.username==cu).first()
            if user:
                user.email=email
                db.session.commit()

                return render_template('profile.html')
            else :flash('修改失败')
    return render_template('modifyprofile.html',form=modform)
if __name__ == '__main__':
    app.run(host="127.0.0.1",debug=True)
