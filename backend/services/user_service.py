from backend.core.security import hash_password
from backend.database.models import User

def create_user(db, user_data):
    password = user_data.password

    print("PASSWORD:", password, type(password))
    if isinstance(password, bytes):
        password = password.decode("utf-8")
        
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must not exceed 72 bytes")

    hashed = hash_password(password)

    user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed,
        role = "user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db,email):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db,username):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db,user_id):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db, user_id, user_data):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
     
    user.username = user_data.username
    user.email = user_data.email

    if user_data.password:
        user.hashed_password = hash_password(user_data.password)

    user.role = getattr(user_data, "role", user.role)

    db.commit()
    db.refresh(user)
    return user
    

def delete_user(db, user_id):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    db.delete(user)
    db.commit()
    return user
