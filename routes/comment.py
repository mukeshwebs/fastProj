from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.comments import CommentCreate, CommentUpdate, CommentResponse
from routes.auth import get_current_user, require_role
from services.comment_service import (
    create_comment_service,
    get_comments_in_post_service,
    get_comment_service,
    update_comment_service,
    delete_comment_service
)
from models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])

#  Create a Comment (Only users can comment)
@router.post("/post/{post_id}", response_model=CommentResponse, dependencies=[Depends(require_role("user"))])
def create_comment(post_id: int, comment_data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to create a comment on a post.
    """
    return create_comment_service(db, post_id, current_user.id, comment_data)


#  Get All Comments in a Post (User or Admin)
@router.get("/post/{post_id}", response_model=list[CommentResponse], dependencies=[Depends(require_role("user", "admin"))])
def get_comments_in_post(post_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to get all comments in a specific post.
    """
    return get_comments_in_post_service(db, post_id)


# Get a Specific Comment by ID (User or Admin)
@router.get("/{comment_id}", response_model=CommentResponse, dependencies=[Depends(require_role("user", "admin"))])
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to get a specific comment by its ID.
    """
    return get_comment_service(db, comment_id)


# Update a Comment (Only Users can update their own comments)
@router.put("/{comment_id}", response_model=CommentResponse, dependencies=[Depends(require_role("user"))])
def update_comment(comment_id: int, comment_data: CommentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to update a comment. Users can only update their own comments.
    """
    comment = get_comment_service(db, comment_id)
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment.")
    
    return update_comment_service(db, comment_id, current_user.id, comment_data)


# Delete a Comment (Only Users can delete their own comments, Admins can delete any comment)
@router.delete("/{comment_id}", dependencies=[Depends(require_role("user", "admin"))])
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to delete a comment. 
    - Users can only delete their own comments.
    - Admins can delete any comment.
    """
    comment = get_comment_service(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if current_user.role != "admin" and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment.")
    
    return delete_comment_service(db, comment_id, current_user.id)
