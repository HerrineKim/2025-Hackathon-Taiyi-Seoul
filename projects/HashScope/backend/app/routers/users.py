from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User
from app.models.deposit import DepositTransaction
from app.schemas.user import UserResponse, UserWithBalance
from app.schemas.deposit import DepositTransactionResponse
from app.auth.dependencies import get_current_user
from app.blockchain.contracts import (
    get_token_balance, 
    get_deposit_balance, 
    verify_deposit_transaction,
    verify_withdraw_transaction,
    DEPOSIT_CONTRACT_ADDRESS,
    HSK_TOKEN_ADDRESS
)

router = APIRouter()

class DepositNotifyRequest(BaseModel):
    transaction_hash: str
    amount: float

class WithdrawNotifyRequest(BaseModel):
    transaction_hash: str
    amount: float

@router.get("/me", response_model=UserWithBalance, summary="Get current user profile")
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    
    Requires authentication via JWT token.
    """
    return current_user

@router.get("/balance", response_model=dict, summary="Get current user token balance")
async def get_token_balance_endpoint(current_user: User = Depends(get_current_user)):
    """
    Get the HSK token balance of the currently authenticated user.
    
    Returns both the on-chain balance and the balance recorded in the database.
    
    Requires authentication via JWT token.
    """
    # Get on-chain balance (optional, can be expensive for frequent calls)
    on_chain_balance = get_token_balance(current_user.wallet_address)
    deposit_balance = get_deposit_balance(current_user.wallet_address)
    
    return {
        "wallet_address": current_user.wallet_address,
        "token_balance": current_user.token_balance,
        "on_chain_balance": on_chain_balance,
        "deposit_balance": deposit_balance,
        "deposit_contract_address": DEPOSIT_CONTRACT_ADDRESS,
        "token_contract_address": HSK_TOKEN_ADDRESS
    }

@router.get("/deposit/info", response_model=dict, summary="Get deposit information")
async def get_deposit_info(current_user: User = Depends(get_current_user)):
    """
    Get information needed to deposit HSK tokens.
    
    Returns the deposit contract address and the user's wallet address.
    
    Requires authentication via JWT token.
    
    ## Contract Addresses
    - **HSK Token Contract**: `0x5073D9411b2179dfeA7c7D8841AF2B3472F8Bf2d`
    - **Deposit Contract**: `0x80304a385F52d256e52C5ADf5779F77F9d291fD2`
    """
    return {
        "wallet_address": current_user.wallet_address,
        "token_contract_address": HSK_TOKEN_ADDRESS,
        "deposit_contract_address": DEPOSIT_CONTRACT_ADDRESS,
        "instructions": "To deposit HSK tokens, first approve the deposit contract to spend your tokens, then call the 'deposit' function on the deposit contract with the amount you want to deposit."
    }

@router.post("/deposit/notify", response_model=dict, summary="Notify backend of token deposit")
async def notify_token_deposit(
    deposit_data: DepositNotifyRequest = Body(...),
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
    
    ## Contract Addresses
    - **HSK Token Contract**: `0x5073D9411b2179dfeA7c7D8841AF2B3472F8Bf2d`
    - **Deposit Contract**: `0x80304a385F52d256e52C5ADf5779F77F9d291fD2`
    """
    # Check if this transaction has already been processed
    existing_tx = db.query(DepositTransaction).filter(
        DepositTransaction.transaction_hash == deposit_data.transaction_hash
    ).first()
    
    if existing_tx:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This transaction has already been processed"
        )
    
    # Verify the transaction on the blockchain
    is_valid, result = verify_deposit_transaction(
        deposit_data.transaction_hash, 
        current_user.wallet_address,
        deposit_data.amount
    )
    
    # Create a deposit transaction record
    deposit_tx = DepositTransaction(
        user_id=current_user.id,
        transaction_hash=deposit_data.transaction_hash,
        amount=deposit_data.amount,
        status="pending"
    )
    
    db.add(deposit_tx)
    db.commit()
    
    if not is_valid:
        deposit_tx.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid deposit transaction: {result}"
        )
    
    # Update the user's token balance
    # If result is a number (amount), use it, otherwise use the amount from the request
    amount_to_add = deposit_data.amount
    if isinstance(result, (int, float)):
        amount_to_add = float(result)
    
    current_user.token_balance += amount_to_add
    deposit_tx.status = "completed"
    db.commit()
    
    return {
        "success": True,
        "new_balance": current_user.token_balance,
        "transaction_hash": deposit_data.transaction_hash,
        "amount_added": amount_to_add
    }

@router.get("/withdraw/info", response_model=dict, summary="Get withdraw information")
async def get_withdraw_info(current_user: User = Depends(get_current_user)):
    """
    Get information needed to withdraw HSK tokens.
    
    Returns the deposit contract address and the user's wallet address.
    
    Requires authentication via JWT token.
    
    ## Contract Addresses
    - **HSK Token Contract**: `0x5073D9411b2179dfeA7c7D8841AF2B3472F8Bf2d`
    - **Deposit Contract**: `0x80304a385F52d256e52C5ADf5779F77F9d291fD2`
    """
    deposit_balance = get_deposit_balance(current_user.wallet_address)
    
    return {
        "wallet_address": current_user.wallet_address,
        "deposit_contract_address": DEPOSIT_CONTRACT_ADDRESS,
        "deposit_balance": deposit_balance,
        "instructions": "To withdraw HSK tokens, call the 'withdraw' function on the deposit contract with the amount you want to withdraw."
    }

@router.post("/withdraw/notify", response_model=dict, summary="Notify backend of token withdrawal")
async def notify_token_withdraw(
    withdraw_data: WithdrawNotifyRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Notify the backend of a token withdrawal transaction.
    
    This endpoint should be called after a successful withdrawal transaction on the blockchain.
    The backend will verify the transaction and update the user's token balance.
    
    - **transaction_hash**: The transaction hash of the withdrawal
    - **amount**: The amount of tokens withdrawn
    
    Requires authentication via JWT token.
    
    ## Contract Addresses
    - **HSK Token Contract**: `0x5073D9411b2179dfeA7c7D8841AF2B3472F8Bf2d`
    - **Deposit Contract**: `0x80304a385F52d256e52C5ADf5779F77F9d291fD2`
    """
    # Check if this transaction has already been processed
    existing_tx = db.query(DepositTransaction).filter(
        DepositTransaction.transaction_hash == withdraw_data.transaction_hash
    ).first()
    
    if existing_tx:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This transaction has already been processed"
        )
    
    # Verify the transaction on the blockchain
    is_valid, result = verify_withdraw_transaction(
        withdraw_data.transaction_hash, 
        current_user.wallet_address,
        withdraw_data.amount
    )
    
    # Create a withdrawal transaction record
    withdraw_tx = DepositTransaction(
        user_id=current_user.id,
        transaction_hash=withdraw_data.transaction_hash,
        amount=-withdraw_data.amount,  # Negative amount for withdrawals
        status="pending"
    )
    
    db.add(withdraw_tx)
    db.commit()
    
    if not is_valid:
        withdraw_tx.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid withdrawal transaction: {result}"
        )
    
    # Update the user's token balance
    # If result is a number (amount), use it, otherwise use the amount from the request
    amount_to_subtract = withdraw_data.amount
    if isinstance(result, (int, float)):
        amount_to_subtract = float(result)
    
    current_user.token_balance -= amount_to_subtract
    withdraw_tx.status = "completed"
    db.commit()
    
    return {
        "success": True,
        "new_balance": current_user.token_balance,
        "transaction_hash": withdraw_data.transaction_hash,
        "amount_withdrawn": amount_to_subtract
    }

@router.get("/deposit/history", response_model=List[DepositTransactionResponse], summary="Get deposit history")
async def get_deposit_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the deposit history for the current user.
    
    Returns a list of deposit transactions.
    
    Requires authentication via JWT token.
    """
    deposits = db.query(DepositTransaction).filter(
        DepositTransaction.user_id == current_user.id
    ).order_by(DepositTransaction.created_at.desc()).all()
    
    return deposits
