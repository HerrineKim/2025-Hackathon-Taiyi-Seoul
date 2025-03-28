from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.database import get_db
from app.models.user import User
from app.models.api_key import APIKey
from app.auth.jwt import verify_token, SECRET_KEY, ALGORITHM

# OAuth2 scheme for JWT token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user from the JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extract wallet address from token
    wallet_address: str = payload.get("sub")
    if wallet_address is None:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_api_key(api_key: str, db: Session = Depends(get_db)):
    """
    Validate API key and return the associated API key object
    """
    # Find API key in database
    api_key_obj = db.query(APIKey).filter(APIKey.key_id == api_key, APIKey.is_active == True).first()
    
    if not api_key_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    return api_key_obj
