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

class UserCreate(UserBase):
    password: str