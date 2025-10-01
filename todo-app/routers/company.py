'''Company Router: Handles CRUD operations for Company entity'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models.base import Company
from schemas import company as schemas_company
from database import get_db

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}}
)

# Create Company
@router.post("/", response_model=schemas_company.Company,status_code=status.HTTP_200_OK)
async def create_company(company: schemas_company.CompanyCreate, db: Session = Depends(get_db)):
    ''' Create a new company first before creating users '''
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
async def list_companies(db: Session = Depends(get_db)):
    ''' List all companies '''
    return db.query(Company).all()
#==========================

# Update Company
@router.put("/{company_id}", response_model=schemas_company.Company,status_code=status.HTTP_200_OK)
def update_company(
    company_id: int,
    company: schemas_company.CompanyUpdate,
    db: Session = Depends(get_db)
    ):
    ''' Update company details '''
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(404, detail="Company ID not found")
    for key, value in company.model_dump().items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company
#==========================

# Delete Company
@router.delete("/{company_id}", status_code=status.HTTP_200_OK)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    ''' Delete a company with ID'''
    db_company = db.query(Company).filter(Company.id == company_id).first()
    company_name = db_company.name if db_company else "N/A"
    if not db_company:
        raise HTTPException(404, detail="Company ID not found")
    db.delete(db_company)
    db.commit()
    return {"message": f"Company ID: {company_id}, name: `{company_name}` \
            has been deleted successfully"}
#==========================
