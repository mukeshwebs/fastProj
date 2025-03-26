from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.comment import Comment
from models.user import User
from models.post import Post
from schemas.comments import CommentCreate, CommentUpdate

#  Create a new comment
def create_comment_service(db: Session, post_id: int, user_id: int, comment_data: CommentCreate):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create the new comment
    new_comment = Comment(content=comment_data.content, user_id=user_id, post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


#  Get all comments for a specific post
def get_comments_in_post_service(db: Session, post_id: int):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments


#  Get a specific comment by ID
def get_comment_service(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


# Update a comment
def update_comment_service(db: Session, comment_id: int, user_id: int, comment_data: CommentUpdate):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Check if user is either the creator of the comment or the creator of the post
    if comment.user_id != user_id:
        post = db.query(Post).filter(Post.id == comment.post_id).first()
        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="User is not authorized to update this comment")

    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment_service(db: Session, comment_id: int, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Check if user is either the creator of the comment or the creator of the post
    if comment.user_id != user_id:
        post = db.query(Post).filter(Post.id == comment.post_id).first()
        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="User is not authorized to delete this comment")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}