from datetime import date
from types import SimpleNamespace

from .models import Booking, Room, User


def compute_dashboard_metrics():
    total_rooms = Room.query.count()
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    available_rooms = Room.query.filter_by(is_available=True).count()
    pending_bookings = Booking.query.filter_by(status="pending").count()
    todays_checkins = Booking.query.filter(
        Booking.start_date == date.today(), Booking.status == "approved"
    ).count()

    return SimpleNamespace(
        total_rooms=total_rooms,
        total_users=total_users,
        total_bookings=total_bookings,
        available_rooms=available_rooms,
        pending_bookings=pending_bookings,
        todays_checkins=todays_checkins,
    )
