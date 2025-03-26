from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.post import PostCreate, PostUpdate, PostResponse
from services.post_service import (
    create_post_service,
    get_posts_in_community_service,
    get_post_service,
    update_post_service,
    delete_post_service
)
from core.security import get_current_user
from models.user import User

router = APIRouter(prefix="/posts", tags=["Posts"])

# ✅ Create a Post (Using Token for User Authentication)
@router.post("/community/{community_id}", response_model=PostResponse)
def create_post(community_id: int, post_data: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to create a post in a community using the authenticated user token.
    """
    return create_post_service(db, community_id, current_user.id, post_data)


# ✅ Get All Posts in a Community
@router.get("/community/{community_id}", response_model=list[PostResponse])
def get_posts_in_community(community_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to retrieve all posts in a specific community.
    """
    return get_posts_in_community_service(db, community_id)


# ✅ Get a Specific Post by Post ID
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to retrieve a specific post by its ID.
    """
    return get_post_service(db, post_id)


# ✅ Update a Post (Using Token for Authorization)
@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to update a post. The authenticated user must be the owner of the post.
    """
    post = update_post_service(db, post_id, current_user.id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized to update this post")
    return post


# ✅ Delete a Post (Using Token for Authorization)
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to delete a post. Only the owner of the post can delete it.
    """
    success = delete_post_service(db, post_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or not authorized to delete this post")
    return {"message": "Post deleted successfully"}
