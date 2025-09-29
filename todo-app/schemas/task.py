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
        from_attributes=True
        
class TaskCreate(TaskBase):
    user_id: int
    
class TaskUpdate(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    priority: Optional[int] = None
    user_id: Optional[int] = None