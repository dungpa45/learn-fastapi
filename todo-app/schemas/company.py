''' Schemas for Company operations '''
from typing import Optional
from pydantic import BaseModel

class CompanyBase(BaseModel):
    ''' Base properties for a Company '''
    name: str
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[int] = None

class Company(CompanyBase):
    ''' Company model with ID '''
    id: int
    class ConfigDict:
        from_attributes=True

class CompanyCreate(CompanyBase):
    ''' Properties required to create a Company '''
    pass

class CompanyUpdate(CompanyBase):
    ''' Properties that can be updated for a Company '''
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[int] = None