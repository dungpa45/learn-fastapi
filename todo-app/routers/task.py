'''Task Router: Handles CRUD operations for Task entity'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models.base import Task, User
from schemas import task as schemas_task
from database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}}
)

# Create Task

@router.post("/", response_model=schemas_task.Task,status_code=status.HTTP_200_OK)
async def create_task(task: schemas_task.TaskCreate, db: Session = Depends(get_db)):
    ''' Create a new task and ensure the user exists '''
    # check user exists
    db_user = db.query(User).filter(User.id == task.user_id).first()
    if not db_user:
        raise HTTPException(400, detail="User does not exist")
    db_task = Task(**task.dict())
    if not db_task:
        raise HTTPException(400, detail="task not exists")

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
#==========================

# List Tasks
@router.get("/", response_model=list[schemas_task.Task])
async def list_tasks(db: Session = Depends(get_db)):
    ''' List all tasks '''
    return db.query(Task).all()
#==========================

# Get All Task by User ID
@router.get("/user/{user_id}", response_model=list[schemas_task.Task])
async def get_tasks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    ''' Get all tasks by User ID '''
    return db.query(Task).filter(Task.user_id == user_id).all()
#==========================

# Get Task by ID
@router.get("/{task_id}", response_model=schemas_task.Task, status_code=status.HTTP_200_OK)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    ''' Get task details by Task ID '''
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(404, detail="task not exists")
    return db_task

# Update Task
@router.put("/{task_id}", response_model=schemas_task.Task,status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: schemas_task.TaskUpdate, db: Session = Depends(get_db)):
    ''' Update task details '''
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(400, detail="task not exists")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task
#==========================

# Delete Task
@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    ''' Delete a task with ID'''
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(404, detail="Task ID not found")
    db.delete(db_task)
    db.commit()
    return {"message": f"Task ID: {task_id} has been deleted successfully"}
#==========================
