from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import Booking, Room


bp = Blueprint("user", __name__)


@bp.route("/rooms")
@login_required
def rooms():
    rooms = Room.query.filter_by(is_available=True).all()
    return render_template("user/rooms.html", rooms=rooms)


@bp.route("/rooms/<int:room_id>")
@login_required
def room_detail(room_id: int):
    room = Room.query.get_or_404(room_id)
    return render_template("user/room_detail.html", room=room)


@bp.route("/rooms/<int:room_id>/book", methods=["POST"])
@login_required
def create_booking(room_id: int):
    room = Room.query.get_or_404(room_id)
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if not start_date or not end_date:
        flash("Please provide both start and end dates.", "warning")
        return redirect(url_for("user.room_detail", room_id=room.id))

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    if end <= start:
        flash("End date must be after start date.", "warning")
        return redirect(url_for("user.room_detail", room_id=room.id))

    if room.is_booked_for_dates(start, end):
        flash("Room already booked for the selected dates.", "danger")
        return redirect(url_for("user.room_detail", room_id=room.id))

    booking = Booking(
        user_id=current_user.id,
        room_id=room.id,
        start_date=start,
        end_date=end,
    )
    db.session.add(booking)
    db.session.commit()
    flash("Booking request submitted. Await confirmation.", "success")
    return redirect(url_for("user.bookings"))


@bp.route("/bookings")
@login_required
def bookings():
    bookings = (
        Booking.query.filter_by(user_id=current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return render_template("user/bookings.html", bookings=bookings)


@bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel_booking(booking_id: int):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash("You can only cancel your own bookings.", "danger")
        return redirect(url_for("user.bookings"))

    booking.cancel()
    db.session.commit()
    flash("Booking cancelled.", "info")
    return redirect(url_for("user.bookings"))
