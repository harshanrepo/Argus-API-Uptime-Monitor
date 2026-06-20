from flask import Blueprint,render_template,session,redirect,request
from database.schema import db,Users,Endpoint
dashboard=Blueprint('dashboard',__name__)

@dashboard.route('/dashboard')
def index():
    return render_template('dashboard.html')

@dashboard.route('/data_add',methods=["POST","GET"])
def add():
    if not 'user_id' in session:
        return redirect('/login')
    if request.method=='POST':
        name=request.form['name']
        url=request.form['url']
        user_exit=Endpoint.query.filter_by(url=url).first()
        if user_exit:
            return 'URL exist already'
        new_endpoint=Endpoint(name=name,url=url,user_id=session['user_id'])
        db.session.add(new_endpoint)
        db.session.commit() 
        return redirect('/dashboard')
    
@dashboard.route('/delete/<int:id>',methods=["POST"])
def delete(id):
    if not 'user_id' in session:
        return redirect('/login')
    endpoint=Endpoint.query.get(id)
    if not endpoint:
        return redirect('/dashboard')
    db.session.delete(endpoint)
    db.session.commit()
    return redirect('/dashboard')