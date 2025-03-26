from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from services.goal_service import (
    create_goal_service,
    get_goals_service,
    get_goal_service,
    update_goal_service,
    delete_goal_service
)
from core.security import get_current_user
from models.user import User

router = APIRouter(prefix="/goals", tags=["Goals"])

# ✅ Create a Goal (User uses token instead of user_id in URL)
@router.post("/", response_model=GoalResponse)
def create_goal(goal_data: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to create a new goal for the authenticated user.
    """
    return create_goal_service(db, current_user.id, goal_data)


# ✅ Get All Goals for the Current User
@router.get("/", response_model=list[GoalResponse])
def get_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to get all goals for the authenticated user.
    """
    return get_goals_service(db, current_user.id)


# ✅ Get a Specific Goal by Goal ID
@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to get a specific goal by its ID for the authenticated user.
    """
    goal = get_goal_service(db, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Goal not found or not authorized to view this goal")
    return goal


# ✅ Update a Goal
@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, goal_data: GoalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to update a goal using the authenticated user token.
    """
    goal = update_goal_service(db, goal_id, current_user.id, goal_data)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found or not authorized to update this goal")
    return goal


# ✅ Delete a Goal
@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to delete a goal using the authenticated user token.
    """
    success = delete_goal_service(db, goal_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found or not authorized to delete this goal")
    return {"message": "Goal deleted successfully"}
