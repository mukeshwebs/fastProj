from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.progress import ProgressCreate, ProgressResponse
from services.progress_service import (
    create_progress_service,
    get_goal_progress_service,
    get_progress_service,
    delete_progress_service
)

router = APIRouter(prefix="/progress", tags=["Progress"])

# Create a Progress Entry
@router.post("/goal/{goal_id}", response_model=ProgressResponse)
def create_progress(goal_id: int, progress_data: ProgressCreate, db: Session = Depends(get_db)):
    return create_progress_service(db, goal_id, progress_data)
# Get All Progress Entries for a Goal
@router.get("/goal/{goal_id}", response_model=list[ProgressResponse])
def get_goal_progress(goal_id: int, db: Session = Depends(get_db)):
    return get_goal_progress_service(db, goal_id)

# Get a Specific Progress Entry
@router.get("/{progress_id}", response_model=ProgressResponse)
def get_progress(progress_id: int, db: Session = Depends(get_db)):
    return get_progress_service(db, progress_id)

# Delete a Progress Entry
@router.delete("/{progress_id}")
def delete_progress(progress_id: int, db: Session = Depends(get_db)):
    return delete_progress_service(db, progress_id)