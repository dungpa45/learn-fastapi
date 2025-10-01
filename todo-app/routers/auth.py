'''Authentication Router: Handles user login and token generation'''
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import auth as schemas_auth
from utils.auth_user import authenticate_user, create_access_token
from database import get_db


router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}}
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# login endpoint
@router.post("/", response_model=schemas_auth.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    ''' User login to get access token '''
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
