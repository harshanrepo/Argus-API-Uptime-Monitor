import os
import scheduler
from flask import Flask, render_template
from database.schema import db
from dotenv import load_dotenv
from routes.auth import auth
from routes.dashboard import dashboard

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(dashboard)

@app.route("/", methods=["GET"])
def base():
    return render_template('base.html')

with app.app_context():
    db.create_all()
    print("Tables created successfully!")
    scheduler.start(app)
    print("Scheduler started!")

if __name__ == '__main__':
    app.run(debug=True)