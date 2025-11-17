# Hotel Booking Manager

Full-stack Flask + SQLite demo that covers guest bookings and an internal admin dashboard. Users can browse rooms, request stays, manage their reservations, and staff members can curate rooms, process bookings, monitor stats, and disable accounts.

## Tech Stack

- Python 3.11+
- Flask, Flask-Login, Flask-SQLAlchemy
- SQLite (file-based `hotel.db`)
- Bootstrap 5 for styling

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m flask --app app:create_app init-db
python -m flask --app app:create_app seed-data
python -m flask --app app:create_app run --debug
```

### Windows quick start

```cmd
windows-run.cmd
```

The script installs the `virtualenv` helper if needed, creates/updates `.venv`, installs dependencies, runs `init-db` + `seed-data`, and launches the Flask dev server bound to `0.0.0.0` so other devices on the same network can reach the LAN URL that the script prints.

Open http://127.0.0.1:5000 and log in. The seed script creates an admin account: `admin@hotel.local` / `admin123`.

## Project Layout

```
app/
  __init__.py          # Flask factory + extensions
  models.py            # User, Booking, Room ORM models
  auth.py              # Registration, login, logout
  user.py              # Guest-facing room + booking flows
  admin.py             # Staff dashboard and management
  commands.py          # CLI helpers (init-db, seed-data)
  utils.py             # Dashboard metrics helpers
  templates/           # Jinja templates for UI panels
  static/css           # Custom styles
config.py              # Config class (SQLite, secret key)
run.py                 # Debug entry point
requirements.txt       # Python dependencies
```

## Feature Highlights

- Role-based navigation (guest/admin) backed by Flask-Login sessions.
- End-to-end booking lifecycle: request → approve/reject → cancel.
- Room CRUD, availability toggle, and pricing controls.
- Staff dashboard with live counts (rooms, bookings, users, check-ins).
- User management table with fast enable/disable toggles.

## Extending

- Replace SQLite URI in `config.py` with Postgres/MySQL if needed.
- Add email notifications by hooking into booking status update forms.
- Guard API with tests using `pytest` + `FlaskClient` fixtures.
