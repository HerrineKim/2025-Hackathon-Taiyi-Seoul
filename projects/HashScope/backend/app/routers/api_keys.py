from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.api_key import APIKey
from app.schemas.api_key import APIKeyCreate, APIKeyResponse, APIKeyWithSecret, APIKeyUsage
from app.auth.dependencies import get_current_user
from app.utils.api_keys import generate_api_key_pair, calculate_expiry_date

router = APIRouter()

@router.post("/", response_model=APIKeyWithSecret, summary="Create new API key")
async def create_api_key(
    api_key_data: APIKeyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new API key for the authenticated user.
    
    - **name**: Optional name for the API key
    - **rate_limit_per_minute**: Optional rate limit per minute (default: 60)
    
    Returns the created API key with the secret key. The secret key will only be shown once.
    
    Requires authentication via JWT token.
    """
    # Check if user has sufficient token balance
    if current_user.token_balance <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient token balance. Please deposit HSK tokens to create API keys."
        )
    
    # Generate API key pair
    key_pair = generate_api_key_pair()
    
    # Create API key in database
    api_key = APIKey(
        key_id=key_pair["key_id"],
        secret_key_hash=key_pair["secret_key_hash"],
        user_id=current_user.id,
        name=api_key_data.name,
        rate_limit_per_minute=api_key_data.rate_limit_per_minute,
        expires_at=calculate_expiry_date(days=365)
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    # Return API key with secret (only shown once)
    return {
        "key_id": api_key.key_id,
        "secret_key": key_pair["secret_key"],  # Only returned once
        "name": api_key.name,
        "is_active": api_key.is_active,
        "created_at": api_key.created_at,
        "expires_at": api_key.expires_at,
        "rate_limit_per_minute": api_key.rate_limit_per_minute
    }

@router.get("/", response_model=List[APIKeyResponse], summary="List all API keys")
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all API keys for the authenticated user.
    
    Returns a list of API keys without the secret keys.
    
    Requires authentication via JWT token.
    """
    api_keys = db.query(APIKey).filter(APIKey.user_id == current_user.id).all()
    return api_keys

@router.get("/{key_id}", response_model=APIKeyResponse, summary="Get API key details")
async def get_api_key(
    key_id: str = Path(..., description="The ID of the API key"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific API key.
    
    - **key_id**: The ID of the API key
    
    Returns the API key details without the secret key.
    
    Requires authentication via JWT token.
    """
    api_key = db.query(APIKey).filter(
        APIKey.key_id == key_id,
        APIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return api_key

@router.get("/{key_id}/usage", response_model=APIKeyUsage, summary="Get API key usage")
async def get_api_key_usage(
    key_id: str = Path(..., description="The ID of the API key"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get usage statistics for a specific API key.
    
    - **key_id**: The ID of the API key
    
    Returns the API key usage statistics.
    
    Requires authentication via JWT token.
    """
    api_key = db.query(APIKey).filter(
        APIKey.key_id == key_id,
        APIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return api_key

@router.delete("/{key_id}", response_model=dict, summary="Delete API key")
async def delete_api_key(
    key_id: str = Path(..., description="The ID of the API key"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific API key.
    
    - **key_id**: The ID of the API key
    
    Returns a success message.
    
    Requires authentication via JWT token.
    """
    api_key = db.query(APIKey).filter(
        APIKey.key_id == key_id,
        APIKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    db.delete(api_key)
    db.commit()
    
    return {"message": "API key deleted successfully"}
