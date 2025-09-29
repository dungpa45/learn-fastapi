from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: Optional[bool] = True  # default active
    is_admin: Optional[bool] = False   # default not admin
    company_id: int

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes=True

class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    company_id: Optional[int] = None
    password: Optional[str] = None