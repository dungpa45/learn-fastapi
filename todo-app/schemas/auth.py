''' Schemas for authentication operations '''
from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    ''' Token model for access token response '''
    access_token: str
    token_type: str

class TokenData(BaseModel):
    ''' Data contained in the token '''
    username: Optional[str] = None
