from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.booking import BookingResponse, BookingUpdate
from routes.auth import get_current_user, require_role
from services.booking_service import (
    create_booking, get_booking, get_user_bookings, update_booking, delete_booking
)
from models.user import User

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# Create Booking (User or Admin)
@router.post("/{session_id}", response_model=BookingResponse, dependencies=[Depends(require_role("user", "admin"))])
def create_booking_route(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to create a new booking.
    The authenticated user's ID will be used instead of passing `user_id`.
    """
    return create_booking(db, current_user.id, session_id)

# Get Booking by ID (User or Admin)
@router.get("/{booking_id}", response_model=BookingResponse, dependencies=[Depends(require_role("user", "admin"))])
def get_booking_route(booking_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to get a booking by ID.
    """
    return get_booking(db, booking_id)

# Get All User Bookings (User or Admin)
@router.get("/", response_model=list[BookingResponse], dependencies=[Depends(require_role("user", "admin"))])
def get_user_bookings_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to get all bookings for the authenticated user.
    """
    return get_user_bookings(db, current_user.id)

# Update Booking (Admin Only)
@router.put("/{booking_id}", response_model=BookingResponse, dependencies=[Depends(require_role("admin"))])
def update_booking_route(booking_id: int, booking_data: BookingUpdate, db: Session = Depends(get_db)):
    """
    API Endpoint to update a booking status.
    Only admins can update bookings.
    """
    return update_booking(db, booking_id, booking_data)

# Delete Booking (Admin Only)
@router.delete("/{booking_id}", dependencies=[Depends(require_role("admin"))])
def delete_booking_route(booking_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to delete a booking.
    Only admins can delete bookings.
    """
    return delete_booking(db, booking_id)
