from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.community import CommunityCreate, CommunityResponse
from services.community_service import (
    create_community,
    get_communities,
    get_community_by_id,
    update_community,
    delete_community,
    add_user_to_community,
    remove_user_from_community
)
from core.security import require_role, get_current_user
from models.user import User

router = APIRouter(prefix="/communities", tags=["Communities"])

# ✅ Create a new community (Trainer or Admin)
@router.post("/", dependencies=[Depends(require_role("trainer", "admin"))], response_model=CommunityResponse)
def create_new_community(community_data: CommunityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to create a new community.
    The user creating the community will be the owner.
    """
    return create_community(db, current_user.id, community_data)


# ✅ Get all communities (Trainer or Admin)
@router.get("/", dependencies=[Depends(require_role("trainer", "admin"))], response_model=list[CommunityResponse])
def list_communities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    API Endpoint to get a list of all communities.
    """
    return get_communities(db, skip, limit)


# ✅ Get a single community by ID (Trainer or Admin)
@router.get("/{community_id}", dependencies=[Depends(require_role("trainer", "admin"))], response_model=CommunityResponse)
def read_community(community_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to get a specific community by its ID.
    """
    community = get_community_by_id(db, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community


# ✅ Update a community (Trainer or Admin)
@router.put("/{community_id}", dependencies=[Depends(require_role("trainer", "admin"))], response_model=CommunityResponse)
def update_existing_community(community_id: int, updated_data: CommunityCreate, db: Session = Depends(get_db)):
    """
    API Endpoint to update a community by its ID.
    """
    community = update_community(db, community_id, updated_data)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community


# ✅ Delete a community (Trainer or Admin)
@router.delete("/{community_id}", dependencies=[Depends(require_role("trainer", "admin"))])
def remove_community(community_id: int, db: Session = Depends(get_db)):
    """
    API Endpoint to delete a community by its ID.
    """
    success = delete_community(db, community_id)
    if not success:
        raise HTTPException(status_code=404, detail="Community not found")
    return {"message": "Community deleted successfully"}


# ✅ Add user to a community (Trainer or Admin)
@router.post("/{community_id}/join", dependencies=[Depends(require_role("trainer", "admin"))])
def join_community(community_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to add the current user to a community using the token.
    """
    success = add_user_to_community(db, community_id, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="User already in the community or community not found")
    return {"message": "User added to community successfully"}


# ✅ Remove user from a community (Trainer, Admin, or User Removing Themselves)
@router.delete("/{community_id}/leave", dependencies=[Depends(require_role("trainer", "admin", "user"))])
def leave_community(community_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    API Endpoint to remove the current user from a community using the token.
    """
    success = remove_user_from_community(db, community_id, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="User not in the community or community not found")
    return {"message": "User removed from community successfully"}
