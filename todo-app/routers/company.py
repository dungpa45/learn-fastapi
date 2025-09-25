from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.base import Company
from schemas import company as schemas_company
from database import get_db

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}}
)

# Create Company
@router.post("/", response_model=schemas_company.Company)
def create_company(company: schemas_company.CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.name == company.name).first()
    if db_company:
        raise HTTPException(400, detail="Company name already exists")
    
    new_company = Company(
        name=company.name,
        description=company.description,
        mode=company.mode,
        rating=company.rating
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company
#==========================

# List Companies
@router.get("/", response_model=list[schemas_company.Company])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()