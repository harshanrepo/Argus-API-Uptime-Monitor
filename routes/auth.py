from flask import Blueprint, request,render_template,redirect,session,flash
auth=Blueprint('auth',__name__)
from database.schema import db,Users 
from werkzeug.security import generate_password_hash, check_password_hash


@auth.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        email=request.form['email']
        password=request.form['password']
        exist_email=Users.query.filter_by(email=email).first()
        if exist_email:
            flash('Email already exists!', 'error')
            return redirect('/register')
        password_hash=generate_password_hash(password)
        new_user=Users(email=email,password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@auth.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        email_exist=Users.query.filter_by(email=email).first()
        if not email_exist:
            flash('User not found!', 'error')
            return redirect('/login')
        hash_password=check_password_hash(email_exist.password_hash,password)
        if hash_password:
            session['user_id']=email_exist.id
            return redirect('/dashboard')
        else:
            flash('Wrong password!', 'error')
            return redirect('/login')
    return render_template('login.html')


@auth.route('/logout',methods=["GET"])
def logout():
    session.clear()
    return redirect('/register')



