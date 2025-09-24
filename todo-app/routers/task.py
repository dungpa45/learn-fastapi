from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.base import Task, User
from schemas import task as schemas_task
from database import get_db
from passlib.context import CryptContext

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}}
)

# Create Task

@router.post("/", response_model=schemas_task.Task)
def create_task(task: schemas_task.TaskCreate, db: Session = Depends(get_db)):
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
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()