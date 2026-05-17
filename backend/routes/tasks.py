from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.dependency import get_db
from backend.schemas.task import TaskCreate, TaskUpdate
from backend.services import task_service
from backend.routes.auth import get_current_user

router = APIRouter(prefix="/tasks")

# CREATE TASK
@router.post("/")
def create_task(
    task_data: TaskCreate, 
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return task_service.create_task(db, task_data, current_user.id)

# GET ALL TASKS
@router.get("/")
def get_tasks(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return task_service.get_tasks(db, current_user.id)

# GET SINGLE TASK
@router.get("/{task_id}")
def get_task(
    task_id: int, 
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = task_service.get_task(db, task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

# UPDATE TASK
@router.put("/{task_id}")
def update_task(
    task_id: int, 
    task_data: TaskUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated_task = task_service.update_task(db, task_id, task_data, current_user.id)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task

# DELETE TASK
@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted_task = task_service.delete_task(db, task_id, current_user.id)

    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}
