from sqlalchemy.orm import Session
from models.community import Community
from models.user import User
from schemas.community import CommunityCreate

#  Create a new community
def create_community(db: Session, user_id: int, community_data: CommunityCreate):
    new_community = Community(
        name=community_data.name,
        description=community_data.description,
        created_by=user_id  # Store the user who created the community
    )
    db.add(new_community)
    db.commit()
    db.refresh(new_community)
    return new_community

#  Get all communities
def get_communities(db: Session, skip: int = 0, limit: int = 10):
    communities = db.query(Community).offset(skip).limit(limit).all()
    for community in communities:
        community.user_ids = [user.id for user in community.users]
    return communities
#  Get a community by ID
def get_community_by_id(db: Session, community_id: int):
    community = db.query(Community).filter(Community.id == community_id).first()
    if community:
        community.user_ids = [user.id for user in community.users]
    return community
#  Update a community
def update_community(db: Session, community_id: int, updated_data: CommunityCreate):
    community = db.query(Community).filter(Community.id == community_id).first()
    if community:
        community.name = updated_data.name
        community.description = updated_data.description
        db.commit()
        db.refresh(community)
    return community

#  Delete a community
def delete_community(db: Session, community_id: int):
    community = db.query(Community).filter(Community.id == community_id).first()
    if community:
        db.delete(community)
        db.commit()
        return True
    return False

#  Add user to a community
def add_user_to_community(db: Session, community_id: int, user_id: int):
    community = db.query(Community).filter(Community.id == community_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not community or not user:
        return False  # Community or user not found
    
    if user in community.users:
        return False  # User already in the community
    
    community.users.append(user)  # Add user to community
    db.commit()
    return True

#  Remove user from a community
def remove_user_from_community(db: Session, community_id: int, user_id: int):
    community = db.query(Community).filter(Community.id == community_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not community or not user:
        return False  # Community or user not found
    
    if user not in community.users:
        return False  # User is not in the community
    
    community.users.remove(user)  # Remove user from community
    db.commit()
    return True