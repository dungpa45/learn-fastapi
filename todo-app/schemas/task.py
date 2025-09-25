from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    summary: str
    description: Optional[str] = None
    status: Optional[bool] = False  # default not completed
    priority: int

class Task(TaskBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True
        
class TaskCreate(TaskBase):
    user_id: int