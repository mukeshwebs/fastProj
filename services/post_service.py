from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.post import Post
from models.user import User
from models.community import Community
from schemas.post import PostCreate, PostUpdate

#  Create a new post
def create_post_service(db: Session, community_id: int, user_id: int, post_data: PostCreate):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if community exists
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    # Check if user is either the creator of the community or a member of the community
    if user.id != community.created_by and user not in community.users:
        raise HTTPException(status_code=403, detail="User is not authorized to create a post in this community")

    # Create the new post
    new_post = Post(content=post_data.content, user_id=user_id, community_id=community_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#  Get all posts in a specific community
def get_posts_in_community_service(db: Session, community_id: int):
    posts = db.query(Post).filter(Post.community_id == community_id).all()
    return posts


#  Get a specific post by ID
def get_post_service(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def update_post_service(db: Session, post_id: int, user_id: int, post_data: PostUpdate):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user is either the creator of the post or the creator of the community
    if post.user_id != user_id:
        community = db.query(Community).filter(Community.id == post.community_id).first()
        if community.created_by != user_id:
            raise HTTPException(status_code=403, detail="User is not authorized to update this post")

    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post
#  Delete a post
def delete_post_service(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user is either the creator of the post or the creator of the community
    if post.user_id != user_id:
        community = db.query(Community).filter(Community.id == post.community_id).first()
        if community.created_by != user_id:
            raise HTTPException(status_code=403, detail="User is not authorized to delete this post")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}