from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, TokenResponse
from core.security import hash_password, verify_password, create_access_token,get_current_user



router = APIRouter(prefix="/auth", tags=["Authentication"])

# User Signup
@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, password_hash=hashed_pwd, role='user')
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    
    return new_user

# User Login
@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

def require_role(*allowed_roles: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            # print(user.role)
            # print(allowed_roles)
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker






