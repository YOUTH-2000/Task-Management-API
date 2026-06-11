from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.core.security import oauth2_scheme

from backend.database.dependency import get_db
from backend.schemas.user import UserCreate, UserLogin
from backend.services.user_service import create_user, get_user_by_email
from backend.core.security import verify_password, create_access_token
from backend.core.config import settings


router = APIRouter(prefix="/auth")

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # hashed_password = hash_password(user_data.password)

    
    # Call the user service to create a new user
    new_user = create_user(db, user_data)
    return {"message": "User registered successfully", "user": new_user}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_current_user(credentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )

        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
 







    