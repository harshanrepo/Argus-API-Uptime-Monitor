from flask import Blueprint,render_template,session,redirect,request
from database.schema import db,Users,Endpoint
dashboard=Blueprint('dashboard',__name__)

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

@dashboard.route('/update/<int:id>',methods=["POST"])
def update(id):
    if 'user_id' not in session:
        return redirect('/login')
    endpoint=Endpoint.query.get(id)
    if not endpoint:
        return redirect('/dashboard')
    endpoint.name = request.form['name']
    endpoint.url = request.form['url']
    db.session.commit()
    return redirect('/dashboard')

@dashboard.route('/dashboard',methods=["GET"])
def display():
    if 'user_id' not in session:
        return redirect('/login')
    view=Endpoint.query.filter_by(user_id=session['user_id']).all()
    return render_template('/dashboard',view=view)