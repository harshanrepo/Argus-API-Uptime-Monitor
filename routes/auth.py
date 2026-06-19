from flask import Blueprint, request,render_template
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
            return "Email already exist"
        password_hash=generate_password_hash(password)
        new_user=Users(email=email,password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
    return render_template('register.html')


@auth.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')