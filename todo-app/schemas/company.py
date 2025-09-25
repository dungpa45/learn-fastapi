from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[int] = None

class Company(CompanyBase):
    id: int
    class Config:
        orm_mode = True

class CompanyCreate(CompanyBase):
    pass
