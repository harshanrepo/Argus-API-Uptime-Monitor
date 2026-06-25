import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from database.schema import Endpoint, Pinglog, db

app = None

def pingall():
    with app.app_context():
        print("Pinging endpoints...")
        endpoints = Endpoint.query.filter_by(is_active=True).all()
        print(f"Found {len(endpoints)} active endpoints")
        for endpoint in endpoints:
            print(f"Pinging {endpoint.url}...")
            try:
                response = requests.get(endpoint.url, timeout=10)
                status_code = response.status_code
                response_time = response.elapsed.total_seconds()
                if status_code == 200:
                    is_up = True
                else:
                    is_up = False
            except:
                status_code = None
                response_time = None
                is_up = False
            log = Pinglog(
                endpoint_id=endpoint.id,
                status_code=status_code,
                response_time=response_time,
                is_up=is_up
            )
            db.session.add(log)
            db.session.commit()
            print(f"Saved log for {endpoint.url} - {status_code}")

scheduler = BackgroundScheduler()
scheduler.add_job(pingall, 'interval', minutes=5)

def start(flask_app):
    global app
    app = flask_app
    scheduler.start()
    print("Running initial ping...")
    with flask_app.app_context():
        pingall()
    print("Initial ping done!")