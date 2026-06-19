from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
db=SQLAlchemy()

class Users(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30),nullable=False,unique=True)
    password_hash=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now())

class Endpoint(db.Model):
    __tablename__='endpoint'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    name=db.Column(db.String(120),nullable=False)
    url=db.Column(db.Text,nullable=False)
    is_active=db.Column(db.Boolean,default=True)
    created_at=db.Column(db.DateTime(timezone=True), server_default=func.now())

class Pinglog(db.Model):
    __tablename__='pinglog'
    id=db.Column(db.Integer,primary_key=True)
    endpoint_id=db.Column(db.Integer,db.ForeignKey('endpoint.id', ondelete='CASCADE'))
    status_code=db.Column(db.Integer)
    response_time=db.Column(db.Float)
    is_up=db.Column(db.Boolean)
    checked_at=db.Column(db.DateTime(timezone=True), server_default=func.now())
