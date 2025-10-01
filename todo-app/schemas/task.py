''' Schemas for Task operations '''
from typing import Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    ''' Base properties for a Task '''
    summary: str
    description: Optional[str] = None
    status: Optional[bool] = False  # default not completed
    priority: int

class Task(TaskBase):
    ''' Task model with ID and user association '''
    id: int
    user_id: int
    class ConfigDict:
        from_attributes=True
        
class TaskCreate(TaskBase):
    ''' Properties required to create a Task '''
    user_id: int
    
class TaskUpdate(BaseModel):
    ''' Properties that can be updated for a Task '''
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    priority: Optional[int] = None
    user_id: Optional[int] = None
