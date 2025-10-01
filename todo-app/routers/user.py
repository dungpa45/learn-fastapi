'''User Router: Handles CRUD operations for User entity'''
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
@router.post("/", response_model=schemas_user.UserResponse,status_code=status.HTTP_200_OK)
async def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    ''' Create a new user who must belong to a company, 
    and the email and username must be unique '''
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
@router.get("/", response_model=list[schemas_user.UserResponse])
async def list_users(db: Session = Depends(get_db)):
    ''' List all users '''
    return db.query(User).all()
#==========================

# get me
@router.get("/me", response_model=schemas_user.UserResponse)
async def get_me(current_user: schemas_user.User = Depends(get_current_user)):
    ''' Get current logged-in user details '''
    return current_user
#==========================

# Get User by ID
@router.get("/{user_id}", response_model=schemas_user.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    ''' Get user details by User ID '''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    return user
#==========================

# Update User
@router.put("/{user_id}", response_model=schemas_user.UserResponse,status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: schemas_user.UserUpdate, db: Session = Depends(get_db)):
    ''' Update user details '''
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
#==========================

# Delete User
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ''' Delete a user with ID'''
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, detail="User not found")
    # Convert SQLAlchemy model to dict with proper type conversion
    user_dict = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "is_active": bool(db_user.is_active),  # Convert int to bool
        "is_admin": bool(db_user.is_admin),    # Convert int to bool
        "company_id": db_user.company_id
    }
    user_data = schemas_user.UserResponse(**user_dict)
    db.delete(db_user)
    db.commit()
    return {
        "message": f"User ID: {user_id} has been deleted successfully",
        "user": user_data
    }
