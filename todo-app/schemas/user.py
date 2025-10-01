''' Schemas for User operations '''
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    ''' Base properties for a User '''
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: Optional[bool] = True  # default active
    is_admin: Optional[bool] = False   # default not admin
    company_id: int

class User(UserBase):
    ''' User model with ID and password '''
    password: str
    id: int
    class ConfigDict:
        from_attributes=True

class UserResponse(UserBase):
    ''' User response model without password '''
    id: int
    class ConfigDict:
        from_attributes=True

class UserCreate(UserBase):
    ''' Properties required to create a User '''
    password: str

class UserUpdate(BaseModel):
    ''' Properties that can be updated for a User '''
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    company_id: Optional[int] = None
    password: Optional[str] = None
