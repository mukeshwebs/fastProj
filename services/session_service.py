from sqlalchemy.orm import Session
from models.session import Session as SessionModel
from models.program import Program as ProgramModel
from models.user import User as UserModel
from schemas.session import SessionCreate
from fastapi import HTTPException, status

# Create a new session
def create_session(db: Session, program_id: int, user_id: int, session_data: SessionCreate):
    # Validate program_id
    program = db.query(ProgramModel).filter(ProgramModel.id == program_id).first()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program with id {program_id} does not exist.")

    # Validate user_id
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist.")

    new_session = SessionModel(
        title=session_data.title,
        description=session_data.description,
        scheduled_at=session_data.scheduled_at,
        program_id=program_id,
        created_by=user_id  # Assigning user_id from path parameter
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# Get all sessions
def get_sessions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SessionModel).offset(skip).limit(limit).all()

# Get a single session by ID
def get_session_by_id(db: Session, program_id: int, session_id: int):
    # Validate program_id
    program = db.query(ProgramModel).filter(ProgramModel.id == program_id).first()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program with id {program_id} does not exist.")

    session = db.query(SessionModel).filter(SessionModel.id == session_id, SessionModel.program_id == program_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session with id {session_id} in program {program_id} does not exist.")
    return session

# Update an existing session
def update_session(db: Session, program_id: int, session_id: int, updated_data: SessionCreate):
    # Validate program_id
    program = db.query(ProgramModel).filter(ProgramModel.id == program_id).first()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program with id {program_id} does not exist.")

    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session with id {session_id} does not exist.")

    session.title = updated_data.title
    session.description = updated_data.description
    session.scheduled_at = updated_data.scheduled_at
    db.commit()
    db.refresh(session)
    return session

# Delete a session
def delete_session(db: Session, program_id: int, session_id: int):
    # Validate program_id
    program = db.query(ProgramModel).filter(ProgramModel.id == program_id).first()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program with id {program_id} does not exist.")

    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session with id {session_id} does not exist.")

    db.delete(session)
    db.commit()
    return True