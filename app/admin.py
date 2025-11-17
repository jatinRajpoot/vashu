from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user

from . import db
from .assets import list_room_images
from .models import Booking, Room, User
from .utils import compute_dashboard_metrics


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
def before_request():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if not current_user.is_admin:
        abort(403)


@bp.route("/dashboard")
def dashboard():
    stats = compute_dashboard_metrics()
    recent_bookings = (
        Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    )
    return render_template("admin/dashboard.html", stats=stats, bookings=recent_bookings)


@bp.route("/rooms")
def rooms():
    rooms = Room.query.order_by(Room.id).all()
    return render_template("admin/rooms.html", rooms=rooms)


@bp.route("/rooms/create", methods=["GET", "POST"])
def create_room():
    available_images = list_room_images()
    default_image = available_images[0] if available_images else ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        room_type = request.form.get("room_type", "").strip()
        price = float(request.form.get("price", 0) or 0)
        description = request.form.get("description", "").strip()
        is_available = bool(request.form.get("is_available"))
        image_filename = request.form.get("image_filename") or default_image or None

        if available_images and image_filename not in available_images:
            flash("Please choose one of the provided room images.", "warning")
            return render_template(
                "admin/room_form.html",
                room=None,
                room_images=available_images,
                selected_image=image_filename,
            )

        room = Room(
            name=name,
            room_type=room_type,
            price=price,
            description=description,
            image_filename=image_filename,
            is_available=is_available,
        )
        db.session.add(room)
        db.session.commit()
        flash("Room added successfully.", "success")
        return redirect(url_for("admin.rooms"))

    return render_template(
        "admin/room_form.html",
        room=None,
        room_images=available_images,
        selected_image=default_image,
    )


@bp.route("/rooms/<int:room_id>/edit", methods=["GET", "POST"])
def edit_room(room_id: int):
    room = Room.query.get_or_404(room_id)
    available_images = list_room_images()
    default_image = room.image_filename or (available_images[0] if available_images else "")

    if request.method == "POST":
        room.name = request.form.get("name", room.name)
        room.room_type = request.form.get("room_type", room.room_type)
        room.price = float(request.form.get("price", room.price))
        room.description = request.form.get("description", room.description)
        room.is_available = bool(request.form.get("is_available"))
        image_filename = request.form.get("image_filename") or default_image or None

        if available_images and image_filename not in available_images:
            flash("Please choose one of the provided room images.", "warning")
            return render_template(
                "admin/room_form.html",
                room=room,
                room_images=available_images,
                selected_image=image_filename,
            )

        room.image_filename = image_filename
        db.session.commit()
        flash("Room updated.", "success")
        return redirect(url_for("admin.rooms"))

    return render_template(
        "admin/room_form.html",
        room=room,
        room_images=available_images,
        selected_image=default_image,
    )


@bp.route("/rooms/<int:room_id>/delete", methods=["POST"])
def delete_room(room_id: int):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    flash("Room removed.", "info")
    return redirect(url_for("admin.rooms"))


@bp.route("/bookings")
def bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin/bookings.html", bookings=bookings)


@bp.route("/bookings/<int:booking_id>/status", methods=["POST"])
def update_booking_status(booking_id: int):
    booking = Booking.query.get_or_404(booking_id)
    status = request.form.get("status", "pending")
    booking.status = status
    db.session.commit()
    flash("Booking status updated.", "success")
    return redirect(url_for("admin.bookings"))


@bp.route("/users")
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@bp.route("/users/<int:user_id>/toggle", methods=["POST"])
def toggle_user(user_id: int):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("Cannot deactivate another admin.", "warning")
        return redirect(url_for("admin.users"))

    user.is_active = not user.is_active
    db.session.commit()
    flash("User status updated.", "info")
    return redirect(url_for("admin.users"))
