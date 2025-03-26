from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.booking import Booking
from models.user import User
from models.session import Session as SessionModel
from schemas.booking import BookingCreate, BookingUpdate

def create_booking(db: Session, user_id: int, program_id: int, session_id: int):
    """
    Create a new booking for a given user, program, and session.
    Ensures a user can't book the same session twice.
    """

    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id, SessionModel.program_id == program_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if the user has already booked this session
    existing_booking = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.session_id == session_id
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="User has already booked this session")

    new_booking = Booking(user_id=user_id, session_id=session_id, confirmed=False)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def get_booking(db: Session, booking_id: int):
    """
    Retrieve a booking by its ID.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

def get_user_bookings(db: Session, user_id: int):
    """
    Retrieve all bookings for a given user.
    """
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def update_booking(db: Session, booking_id: int, booking_data: BookingUpdate):
    """
    Update a booking's status.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = booking_data.status
    db.commit()
    db.refresh(booking)
    return booking

def delete_booking(db: Session, booking_id: int):
    """
    Delete a booking by its ID.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}