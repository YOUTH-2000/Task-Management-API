from pydantic import BaseModel, Field
from backend.schemas.enums import StatusEnum, PriorityEnum
from datetime import datetime
from typing import Optional

# Create task
class TaskCreate(BaseModel):
    title: str  = Field(min_length=1, max_length=100)
    description: str = ""
    status: StatusEnum
    priority: PriorityEnum
    
# Update task
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    
# Output schema for task
class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    created_at:datetime
    updated_at:datetime
    owner_id: int

    class Config:
        from_attributes = True

