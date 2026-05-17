from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from jose import jwt
from datetime import datetime, timedelta
from backend.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes = settings.access_token_expire_minutes
    )
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



