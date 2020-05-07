# -*- coding: utf-8 -*-
from configs import db,loginmanager,app#,photos
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
@login_required
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
                return  redirect(url_for('profile'))
    return  render_template('login.html',loginform=loginform)
@app.route('/register',methods=['GET','POST'])
def register():
    regform=RegisterForm()
    if request.method=='POST':
        if(regform.validate_on_submit()):
            username = request.form.get('username')
            password = request.form.get('password')
            email=request.form.get('email')
            user=User(username,password,email)
            db.session.add(user)
            db.session.commit()
            return  'reg success'
        else : return 'fail'
    return  render_template('register.html',regform=regform)
@app.route('/findbook',methods=['GET','POST'])
@login_required
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
@app.route('/borrowbook/<isbn>')
@login_required
def borrowbook(isbn):
    book=Book.query.filter(Book.isbn==isbn).first()
    if book:
        if book.num>=1 and current_user.js==1 and book.borrowable==1:
            book.num=book.num-1
            current_user.js=0
            current_user.bid=book.id
            if book.num==0:
                book.borrowable=0
            db.session.commit()
            flash('借书成功')
        else :flash('借书失败')
    return redirect(url_for('profile'))


@app.route('/returnbook/<bid>')
@login_required
def returnbook(bid):
    book=Book.query.filter(Book.id==bid).first()
    if book:
        current_user.js=1
        current_user.bid=0
        book.num=book.num+1
        if(book.num>=1):
            book.borrowable=1
        db.session.commit()
        flash('还书成功')
    else:
        flash('还书失败')
    return redirect(url_for('profile'))
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
    uploadform=UploadForm()
    if request.method=="POST":
        if uploadform.validate_on_submit():
            file=request.files['file']
            file.save(os.path.join(upload_dir,file.filename))
            if(file.filename==""):
                filename="default.jpg"
            else:    filename=file.filename
            user=User.query.filter(User.username==current_user.username).first()
            if user:
                url = "/upload/"+filename
                user.url=url
                db.session.commit()
                return redirect(url_for('profile'))
    return render_template('upload.html',form=uploadform)
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
                redirect(url_for('profile'))
            else :flash('修改失败')
    return render_template('modifyprofile.html',form=modform)
@app.route('/manageuser',methods=['GET','POST'])
@login_required
def manageuser():
    if current_user.status==1:
        users=User.query.filter(User.status!=1).all()
        return render_template('manageuser.html', users=users)
    return 'permission denied'
@app.route('/managebook',methods=['GET','POST'])
@login_required
def managebook():
    if current_user.status==1:
        books=Book.query.all()
        return render_template('managebook.html',books=books)
    return 'permission denied'
@app.route('/deleteuser/<uid>',methods=['GET','POST'])
@login_required
def deleteuser(uid):
    if current_user.status==1:
        user = User.query.filter(User.id == uid).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('删除用户成功')
            users = User.query.filter(User.status != 1).all()
            books = Book.query.all()
            return render_template('manageuser.html', users=users, books=books)
    return  'permission denied'
@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    book = Book.query.filter(Book.id == current_user.bid).first()
    user=User.query.filter(User.username==current_user.username).first()
    url=user.url
    return render_template('profile.html',book=book,url=url)
if __name__ == '__main__':
    app.run(host="127.0.0.1",debug=True)
