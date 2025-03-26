from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.progress import Progress
from models.goal import Goal
from schemas.progress import ProgressCreate
from models.achievements import Achievement
from schemas.progress import ProgressCreate
from schemas.achievements import AchievementCreate

# Create a Progress Entry
# Create a Progress Entry
def create_progress_service(db: Session, goal_id: int, progress_data: ProgressCreate):
    # Check if goal exists
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    new_progress = Progress(**progress_data.dict(), goal_id=goal_id)
    goal.current_value += progress_data.value

    # Check if the goal is achieved
    if goal.current_value >= goal.target_value:
        goal.achieved = True
        # Create an achievement
        achievement_data = AchievementCreate(
            title="Goal Achieved",
            description=f"Successfully achieved the goal: {goal.title}"
        )
        new_achievement = Achievement(**achievement_data.dict(), goal_id=goal_id)
        db.add(new_achievement)

    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return new_progress
# Get All Progress Entries for a Goal
def get_goal_progress_service(db: Session, goal_id: int):
    progress_entries = db.query(Progress).filter(Progress.goal_id == goal_id).all()
    if not progress_entries:
        raise HTTPException(status_code=404, detail="No progress entries found for this goal")
    return progress_entries

# Get a Specific Progress Entry
def get_progress_service(db: Session, progress_id: int):
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    return progress

# Delete a Progress Entry
def delete_progress_service(db: Session, progress_id: int):
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")

    db.delete(progress)
    db.commit()
    return {"message": "Progress entry deleted successfully"}