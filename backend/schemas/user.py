from pydantic import BaseModel, EmailStr, Field

# Used for user registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


# Used for Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str  = Field(min_length=6, max_length=72)

# Return to client after registration or login
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    
    class Config:
        from_attributes = True


