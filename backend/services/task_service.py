from backend.database.models import Task

# CREATE TASK
def create_task(db, task_data, user_id):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        owner_id=user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# GET ALL TASKS(only current user)
def get_tasks(db, user_id):
    return db.query(Task).filter(Task.owner_id == user_id).all()

# GET SINGLE TASK
def get_task(db, task_id, user_id):
    return db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

# UPDATE TASK
def update_task(db, task_id, task_data, user_id):
    task = get_task(db, task_id, user_id)
    if not task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

# DELETE TASK
def delete_task(db, task_id, user_id):
    task = get_task(db, task_id, user_id)
    if not task:
        return None

    db.delete(task)
    db.commit()
    return task        