from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.goal import Goal
from models.user import User
from schemas.goal import GoalCreate, GoalUpdate

# Create a Goal
def create_goal_service(db: Session, user_id: int, goal_data: GoalCreate):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_goal = Goal(**goal_data.dict(), user_id=user_id)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

# Get All Goals for a User
def get_goals_service(db: Session, user_id: int):
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    if not goals:
        raise HTTPException(status_code=404, detail="No goals found")
    return goals

# Get a Specific Goal
def get_goal_service(db: Session, goal_id: int):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

# Update a Goal
def update_goal_service(db: Session, goal_id: int, user_id: int, goal_data: GoalUpdate):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Check if the user is the creator of the goal
    if goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="User is not authorized to update this goal")

    if goal_data.current_value is not None:
        goal.current_value = goal_data.current_value
    if goal_data.target_value is not None:
        goal.target_value = goal_data.target_value
    if goal_data.achieved is not None:
        goal.achieved = goal_data.achieved
    
    db.commit()
    db.refresh(goal)
    return goal

# Delete a Goal
def delete_goal_service(db: Session, goal_id: int, user_id: int):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Check if the user is the creator of the goal
    if goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="User is not authorized to delete this goal")

    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}
