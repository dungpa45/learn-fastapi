from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.base import User
from schemas import auth as schemas_auth, user as schemas_user
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import get_db
from jose import JWTError, jwt
import logging
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# get user from db
def get_user(user: schemas_user.User, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

# authenticate user
def authenticate_user(db: Session, user_name: str, password: str):
    user = db.query(User).filter(User.username == user_name).first()
    if not user or not verify_password(password, user.password):
        return False
    return user

# create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info(f"Received token: {token[:20]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = str(payload.get("sub"))
        logger.info(f"Decoded username: {username}")
        if username is None:
            raise credentials_exception
        token_data = schemas_auth.TokenData(username=username)
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credentials_exception
    # user = get_user(username, db=db)
    user = db.query(User).filter(User.username == token_data.username).first()
    logger.info(f"Found user: {user.username if user else 'None'}")
    if user is None:
        raise credentials_exception
    return user