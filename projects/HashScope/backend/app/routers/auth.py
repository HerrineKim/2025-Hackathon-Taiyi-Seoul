from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import secrets
import string

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import NonceRequest, NonceResponse, VerifySignatureRequest, TokenResponse
from app.auth.wallet import create_auth_message, verify_signature, generate_nonce
from app.auth.jwt import create_access_token

router = APIRouter()

@router.post("/nonce", response_model=NonceResponse, summary="Get authentication nonce")
async def get_nonce(request: NonceRequest, db: Session = Depends(get_db)):
    """
    Get a nonce for wallet authentication.
    
    - **wallet_address**: Ethereum wallet address
    
    Returns a nonce and message to be signed by the wallet.
    """
    # Normalize wallet address
    wallet_address = request.wallet_address.lower()
    
    # Check if user exists
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    
    # Generate new nonce
    nonce = generate_nonce()
    
    if user:
        # Update existing user's nonce
        user.nonce = nonce
    else:
        # Create new user
        user = User(wallet_address=wallet_address, nonce=nonce)
        db.add(user)
    
    db.commit()
    
    # Create message to be signed
    message = create_auth_message(wallet_address, nonce)
    
    return NonceResponse(
        wallet_address=wallet_address,
        nonce=nonce,
        message=message
    )

@router.post("/verify", response_model=TokenResponse, summary="Verify wallet signature")
async def verify_wallet_signature(request: VerifySignatureRequest, db: Session = Depends(get_db)):
    """
    Verify wallet signature and issue JWT token.
    
    - **wallet_address**: Ethereum wallet address
    - **signature**: Signature of the nonce message
    
    Returns a JWT token if signature is valid.
    """
    # Normalize wallet address
    wallet_address = request.wallet_address.lower()
    
    # Get user from database
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid wallet address"
        )
    
    # Create message that should have been signed
    message = create_auth_message(wallet_address, user.nonce)
    
    # Verify signature
    if not verify_signature(message, request.signature, wallet_address):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        )
    
    # Generate new nonce for security (prevent replay attacks)
    user.nonce = generate_nonce()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": wallet_address})
    
    return TokenResponse(
        access_token=access_token,
        wallet_address=wallet_address,
        token_balance=user.token_balance
    )
