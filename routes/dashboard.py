from flask import Blueprint,render_template,session,redirect,request
from database.schema import db,Users,Endpoint,Pinglog
dashboard=Blueprint('dashboard',__name__)

@dashboard.route('/data_add', methods=["POST", "GET"])
def add():
    if not 'user_id' in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        user_exit = Endpoint.query.filter_by(url=url).first()
        if user_exit:
            return 'URL exist already'
        new_endpoint = Endpoint(name=name, url=url, user_id=session['user_id'])
        db.session.add(new_endpoint)
        db.session.commit()

        from scheduler import pingall
        pingall()

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

@dashboard.route('/update/<int:id>',methods=["POST","GET"])
def update(id):
    if 'user_id' not in session:
        return redirect('/login')
    endpoint=Endpoint.query.get(id)
    if not endpoint:
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template('update.html', endpoint=endpoint)
    if request.method == 'POST':
        endpoint.name = request.form['name']
        endpoint.url = request.form['url']
        db.session.commit()
        return redirect('/dashboard')

@dashboard.route('/dashboard',methods=["GET"])
def display():
    if 'user_id' not in session:
        return redirect('/login')
    endpoints = Endpoint.query.filter_by(user_id=session['user_id']).all()
    logs = {}
    for endpoint in endpoints:
        latest_log = Pinglog.query.filter_by(endpoint_id=endpoint.id).order_by(Pinglog.checked_at.desc()).first()
        logs[endpoint.id] = latest_log
    total=len(endpoints)
    up = sum(1 for log in logs.values() if log and log.is_up == True)
    down = sum(1 for log in logs.values() if log and log.is_up == False)
    times = [log.response_time for log in logs.values() if log and log.response_time]
    avg_time = round(sum(times) / len(times), 2) if times else 0
    return render_template('dashboard.html',endpoints=endpoints,logs=logs,total=total,up=up,down=down,avg_time=avg_time)