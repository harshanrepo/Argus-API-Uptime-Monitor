# Argus — Your Silent API Guardian

Argus is a self-hosted API uptime monitoring tool. It pings your endpoints every 5 minutes, logs status codes and response times, and shows live UP/DOWN status on a clean dashboard.

Designed and developed end-to-end (UI in Figma, then built) by **Shri Harshan M**.

---

## Features

- **Auto Pinging** — background scheduler checks all active endpoints every 5 minutes
- **Live Status** — instant UP/DOWN view per endpoint (based on HTTP 200 response)
- **Response Time Tracking** — logs latency for every ping
- **Auth** — email/password registration & login with hashed passwords
- **Dashboard** — add, edit, delete monitored endpoints; view total/up/down counts and average response time
- **Client-side search** — filter endpoints by name/URL instantly

---

## Tech Stack

| Layer          | Tech                                  |
|----------------|----------------------------------------|
| Backend        | Flask (Blueprints)                     |
| Database       | PostgreSQL (via SQLAlchemy ORM)        |
| Scheduling     | APScheduler (`BackgroundScheduler`)    |
| Auth           | Werkzeug (`generate_password_hash`)    |
| Frontend       | Jinja2 templates + Tailwind CSS        |
| Font           | Space Grotesk                          |
| Hosting        | Render                                 |

---

## Project Structure

```
argus/
├── app.py                  # App factory, config, scheduler bootstrap
├── scheduler.py             # Background ping job (every 5 min)
├── routes/
│   ├── auth.py               # /register, /login, /logout
│   └── dashboard.py          # /dashboard, /data_add, /update, /delete
├── database/
│   └── schema.py             # SQLAlchemy models: Users, Endpoint, Pinglog
├── templates/
│   ├── base.html              # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── update.html
└── static/
    └── favicon.png
```

> Note: `database/schema.py` isn't included in this README's source files — add its model fields here if you want the schema documented too.

---

## How It Works

1. On app startup, `scheduler.start(app)` runs an initial ping and starts a background job that pings every active endpoint every 5 minutes.
2. Each ping records a `Pinglog` entry — status code, response time, and an `is_up` flag (`True` only on HTTP 200).
3. The dashboard reads the **latest** log per endpoint to show live status, and aggregates totals (up/down count, average response time).
4. Adding a new endpoint triggers an immediate ping so status isn't stale until the next 5-minute cycle.

---

## Setup

### 1. Clone & install dependencies
```bash
git clone https://github.com/harshanrepo/argus.git
cd argus
pip install flask flask-sqlalchemy apscheduler requests python-dotenv psycopg2-binary werkzeug
```

### 2. Environment variables
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>
SECRET_KEY=your-secret-key-here
```

### 3. Run locally
```bash
python app.py
```
The app runs at `http://localhost:5000` with `db.create_all()` auto-creating tables on startup.

---

## Routes

| Method | Route                | Description                          |
|--------|-----------------------|---------------------------------------|
| GET    | `/`                    | Landing page                          |
| GET/POST | `/register`          | Create account                        |
| GET/POST | `/login`              | Log in                                |
| GET    | `/logout`              | Clear session                         |
| GET    | `/dashboard`            | View monitored endpoints & stats      |
| POST   | `/data_add`             | Add a new endpoint (triggers instant ping) |
| GET/POST | `/update/<id>`        | Edit an endpoint                      |
| POST   | `/delete/<id>`          | Remove an endpoint                    |

---

## Links

- **LinkedIn:** https://www.linkedin.com/in/mrshri-harshan/

---

© 2026 Argus. All rights reserved.
