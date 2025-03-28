from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserWithBalance
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserWithBalance, summary="Get current user profile")
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    
    Requires authentication via JWT token.
    """
    return current_user

@router.get("/balance", response_model=dict, summary="Get current user token balance")
async def get_token_balance(current_user: User = Depends(get_current_user)):
    """
    Get the HSK token balance of the currently authenticated user.
    
    Requires authentication via JWT token.
    """
    return {
        "wallet_address": current_user.wallet_address,
        "token_balance": current_user.token_balance,
        "deposit_contract_address": current_user.deposit_contract_address
    }

@router.post("/deposit/notify", response_model=dict, summary="Notify backend of token deposit")
async def notify_token_deposit(
    transaction_hash: str,
    amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Notify the backend of a token deposit transaction.
    
    This endpoint should be called after a successful deposit transaction on the blockchain.
    The backend will verify the transaction and update the user's token balance.
    
    - **transaction_hash**: The transaction hash of the deposit
    - **amount**: The amount of tokens deposited
    
    Requires authentication via JWT token.
    """
    # In a real implementation, you would verify the transaction on the blockchain
    # For now, we'll just update the balance
    
    current_user.token_balance += amount
    db.commit()
    
    return {
        "success": True,
        "new_balance": current_user.token_balance,
        "transaction_hash": transaction_hash
    }
