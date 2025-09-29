from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette import status
from database import get_db
from models.base import User, Company
from schemas import user as schemas_user
from utils.auth_user import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create User
@router.post("/", response_model=schemas_user.User,status_code=status.HTTP_200_OK)
async def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    # Check company first
    db_company = db.query(Company).filter(Company.id == user.company_id).first()
    if not db_company:
        raise HTTPException(400, detail="Company does not exist")

    # Check if user exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(400, detail="Username already registered")
    
    # Check if email exists
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(user.password)
    new_user = User(
        username=user.username, 
        email=user.email, 
        password=hashed_pw,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        company_id=user.company_id
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#==========================

# List Users
@router.get("/", response_model=list[schemas_user.User])
async def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
#==========================

# get me
@router.get("/me", response_model=schemas_user.User)
async def get_me(current_user: schemas_user.User = Depends(get_current_user)):
    return current_user
#==========================

# Get User by ID
@router.get("/{user_id}", response_model=schemas_user.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    return user
#==========================

# Update User
@router.put("/{user_id}", response_model=schemas_user.User,status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: schemas_user.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, detail="User not found")
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
#==========================

# Delete User
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, detail="User not found")
    user_data = schemas_user.User.from_orm(db_user)
    db.delete(db_user)
    db.commit()
    return {
        "message": f"User ID: {user_id} has been deleted successfully",
        "user": user_data
    }