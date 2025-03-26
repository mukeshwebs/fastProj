from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.session import SessionCreate, SessionResponse
from services.session_service import (
    create_session,
    get_sessions,
    get_session_by_id,
    update_session,
    delete_session,
)
from core.security import require_role, get_current_user
from models.user import User

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# ✅ Create a New Session (Using JWT for User Authentication)
@router.post("/{program_id}/create", dependencies=[Depends(require_role("trainer", "admin"))], response_model=SessionResponse)
def create_new_session(program_id: int, session_data: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to create a new session. Only trainers or admins are allowed.
    """
    return create_session(db, program_id, current_user.id, session_data)

# ✅ Get All Sessions with Pagination
@router.get("/", dependencies=[Depends(require_role("trainer", "admin"))], response_model=list[SessionResponse])
def list_sessions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    API Endpoint to fetch all sessions with optional pagination.
    """
    return get_sessions(db, skip, limit)

# ✅ Get a Single Session by Program and Session ID
@router.get("/{program_id}/{session_id}", dependencies=[Depends(require_role("trainer", "admin"))], response_model=SessionResponse)
def read_session(program_id: int, session_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to retrieve a session using program ID and session ID.
    """
    session = get_session_by_id(db, program_id, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# ✅ Update a Session (Only for Trainers or Admins)
@router.put("/{program_id}/{session_id}", dependencies=[Depends(require_role("trainer", "admin"))], response_model=SessionResponse)
def update_existing_session(program_id: int, session_id: int, updated_data: SessionCreate, db: Session = Depends(get_db)):
    """
    API Endpoint to update an existing session by session ID and program ID.
    """
    session = update_session(db, program_id, session_id, updated_data)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# ✅ Delete a Session (Only for Trainers or Admins)
@router.delete("/{program_id}/{session_id}", dependencies=[Depends(require_role("trainer", "admin"))])
def remove_session(program_id: int, session_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to delete a session using program ID and session ID.
    """
    success = delete_session(db, program_id, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}
