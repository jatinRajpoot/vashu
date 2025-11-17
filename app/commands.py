import click
from flask import current_app
from flask.cli import with_appcontext

from . import db
from .models import User, Room


def init_db() -> None:
    db.drop_all()
    db.create_all()


def seed_data() -> None:
    if not User.query.filter_by(email="admin@hotel.local").first():
        admin = User(name="Admin", email="admin@hotel.local", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)

    if Room.query.count() == 0:
        sample_rooms = [
            Room(
                name="Deluxe Suite",
                room_type="Suite",
                price=220.0,
                description="Spacious suite with ocean view.",
                image_filename="rooms1.jpg",
            ),
            Room(
                name="Standard Room",
                room_type="Standard",
                price=120.0,
                description="Cozy room perfect for solo travelers.",
                image_filename="rooms2.jpg",
            ),
            Room(
                name="Family Room",
                room_type="Family",
                price=180.0,
                description="Ideal for families up to four guests.",
                image_filename="rooms3.jpg",
            ),
        ]
        db.session.add_all(sample_rooms)

    db.session.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Database initialized")


@click.command("seed-data")
@with_appcontext
def seed_data_command():
    seed_data()
    click.echo("Sample data inserted")


def register_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_data_command)
