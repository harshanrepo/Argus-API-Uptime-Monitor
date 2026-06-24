import requests
from apscheduler.schedulers.background import BackgroundScheduler
from database.schema import Endpoint, Pinglog, db

def pingall():
    endpoints=Endpoint.query.filter_by(is_active=True).all()
    for endpoint in endpoints:
        try:
            response=requests.get(endpoint.url,timeout=10)
            status_code=response.status_code
            response_time=response.elapsed.total_seconds()
            if status_code == 200:
                is_up=True
            else:
                is_up=False
        except:
            status_code=None
            response_time=None
            is_up=False
        log=Pinglog(endpoint_id=endpoint.id,status_code=status_code,response_time=response_time,is_up=is_up)
        db.session.add(log)
        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(pingall, 'interval', minutes=5)

def start():
    scheduler.start()

