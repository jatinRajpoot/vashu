from flask import Blueprint, render_template

from .models import Room


bp = Blueprint("landing", __name__)


@bp.route("/")
def home():
    featured_rooms = (
        Room.query.filter_by(is_available=True)
        .order_by(Room.price.desc())
        .limit(6)
        .all()
    )
    return render_template("site/landing.html", rooms=featured_rooms)
