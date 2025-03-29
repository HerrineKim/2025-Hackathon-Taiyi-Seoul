from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
import os
from datetime import datetime

from app.database import get_db
from app.models import User, Transaction
from app.blockchain.contracts import (
    get_balance, 
    get_contract_balance,
    get_wallet_balance,
    verify_deposit_transaction, 
    verify_withdraw_transaction,
    verify_usage_deduction_transaction,
    get_transaction_status,
    build_deposit_transaction,
    sign_transaction,
    wei_to_hsk,
    hsk_to_wei,
    format_wei_to_hsk
)
from app.auth.dependencies import get_current_user, get_current_admin_user

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# 사용자 스키마
class UserResponse(BaseModel):
    wallet_address: str
    balance: int = 0
    is_admin: bool = False
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 트랜잭션 스키마
class TransactionCreate(BaseModel):
    user_wallet: str
    tx_hash: str
    amount: int
    tx_type: str = "deposit"
    status: str = "pending"

# 예치 요청 스키마
class DepositRequest(BaseModel):
    wallet_address: str
    amount: int

# 서명 요청 스키마
class SignTransactionRequest(BaseModel):
    wallet_address: str
    amount: int
    private_key: str = Field(..., description="개인 키는 서버에 저장되지 않으며 트랜잭션 서명에만 사용됩니다")

# 서명 응답 스키마
class SignTransactionResponse(BaseModel):
    tx_hash: str
    amount: int
    message: str

# 예치 응답 스키마
class DepositResponse(BaseModel):
    message: str
    deposit_address: str
    amount: int

# 인출 요청 스키마
class WithdrawRequest(BaseModel):
    wallet_address: str
    amount: int

# 인출 응답 스키마
class WithdrawResponse(BaseModel):
    message: str
    request_id: int

# 인출 정보 응답 스키마
class WithdrawInfoResponse(BaseModel):
    message: str
    deposit_contract: str

# 사용량 차감 요청 스키마
class UsageDeductRequest(BaseModel):
    wallet_address: str
    amount: int
    recipient_address: str

# 사용량 차감 응답 스키마
class UsageDeductResponse(BaseModel):
    message: str
    request_id: int

# 트랜잭션 알림 스키마
class TransactionNotify(BaseModel):
    tx_hash: str
    tx_type: str = "deposit"  # deposit, withdraw, usage

# 트랜잭션 상태 응답 스키마
class TransactionStatusResponse(BaseModel):
    status: str
    message: Optional[str] = None

# 사용자 목록 조회
@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# 사용자 상세 조회
@router.get("/{wallet_address}", response_model=UserResponse)
def read_user(wallet_address: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 사용자 잔액 조회
@router.get("/{wallet_address}/balance")
def read_user_balance(wallet_address: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 블록체인에서 실제 잔액 조회
    balance = get_balance(wallet_address)
    
    return {
        "wallet_address": wallet_address,
        "balance_wei": balance,
        "balance_hsk": wei_to_hsk(balance),
        "formatted_balance": format_wei_to_hsk(balance)
    }

# 예치 정보 조회
@router.get("/deposit/info", response_model=DepositResponse)
def get_deposit_info():
    deposit_contract = os.getenv("DEPOSIT_CONTRACT_ADDRESS")
    return {
        "message": "아래 주소로 HSK를 전송하여 예치할 수 있습니다.",
        "deposit_address": deposit_contract,
        "amount": 0
    }

# 트랜잭션 서명 및 전송
@router.post("/deposit/sign", response_model=SignTransactionResponse)
async def sign_deposit_transaction(
    request: SignTransactionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    사용자의 개인 키를 사용하여 예치 트랜잭션에 서명하고 전송합니다.
    
    - **wallet_address**: 사용자 지갑 주소
    - **amount**: 예치할 금액 (wei 단위)
    - **private_key**: 개인 키 (서버에 저장되지 않음)
    
    Returns:
        서명된 트랜잭션 해시
    """
    # 사용자 인증 확인
    if current_user.wallet_address.lower() != request.wallet_address.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only sign transactions for your own wallet"
        )
    
    try:
        # 트랜잭션 생성
        tx = build_deposit_transaction(
            from_address=request.wallet_address,
            amount_wei=request.amount
        )
        
        # 트랜잭션 서명 및 전송
        tx_hash = sign_transaction(request.private_key, tx)
        
        return {
            "tx_hash": tx_hash,
            "amount": request.amount,
            "message": f"트랜잭션이 성공적으로 서명되어 전송되었습니다. 트랜잭션 해시: {tx_hash}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"트랜잭션 서명 중 오류가 발생했습니다: {str(e)}"
        )

# 예치 트랜잭션 알림
@router.post("/deposit/notify", response_model=TransactionStatusResponse)
def notify_deposit_transaction(tx_data: TransactionNotify, db: Session = Depends(get_db)):
    try:
        # 트랜잭션 검증
        verification = verify_deposit_transaction(tx_data.tx_hash)
        
        if verification["success"]:
            # 사용자 조회
            user = db.query(User).filter(User.wallet_address == verification["user"]).first()
            
            if not user:
                # 새 사용자 생성
                user = User(
                    username=f"user_{verification['user'][:8]}",
                    email=f"user_{verification['user'][:8]}@example.com",
                    wallet_address=verification["user"]
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            
            # 트랜잭션 기록
            tx = Transaction(
                user_wallet=user.wallet_address,
                tx_hash=tx_data.tx_hash,
                amount=verification["amount"],
                tx_type="deposit",
                status="confirmed"
            )
            db.add(tx)
            db.commit()
            
            return {"status": "success", "message": "Deposit transaction verified and recorded"}
        else:
            return {"status": "failed", "message": verification["message"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 인출 정보 조회
@router.get("/withdraw/info", response_model=WithdrawInfoResponse)
def get_withdraw_info():
    deposit_contract = os.getenv("DEPOSIT_CONTRACT_ADDRESS")
    return {
        "message": "인출은 관리자만 수행할 수 있습니다. 인출 요청을 제출하면 관리자가 처리합니다.",
        "deposit_contract": deposit_contract
    }

# 인출 요청
@router.post("/withdraw/request", response_model=WithdrawResponse)
def request_withdraw(
    request: WithdrawRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 사용자 인증 확인
    if current_user.wallet_address.lower() != request.wallet_address.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only request withdrawals for your own wallet"
        )
    
    # 잔액 확인
    balance = get_balance(request.wallet_address)
    if balance < request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. Available: {balance}, Requested: {request.amount}"
        )
    
    # 인출 요청 기록
    tx = Transaction(
        user_wallet=current_user.wallet_address,
        tx_hash="pending",
        amount=request.amount,
        tx_type="withdraw_request",
        status="pending"
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    
    return {"message": "Withdrawal request submitted successfully", "request_id": tx.id}

# 인출 트랜잭션 알림
@router.post("/withdraw/notify", response_model=TransactionStatusResponse)
def notify_withdraw_transaction(
    tx_data: TransactionNotify, 
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    try:
        # 트랜잭션 검증
        verification = verify_withdraw_transaction(tx_data.tx_hash)
        
        if verification["success"]:
            # 사용자 조회
            user = db.query(User).filter(User.wallet_address == verification["user"]).first()
            
            if not user:
                return {"status": "failed", "message": "User not found"}
            
            # 트랜잭션 기록
            tx = Transaction(
                user_wallet=user.wallet_address,
                tx_hash=tx_data.tx_hash,
                amount=verification["amount"],
                tx_type="withdraw",
                status="confirmed"
            )
            db.add(tx)
            db.commit()
            
            return {"status": "success", "message": "Withdraw transaction verified and recorded"}
        else:
            return {"status": "failed", "message": verification["message"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 사용량 차감 요청
@router.post("/usage/deduct", response_model=UsageDeductResponse)
def deduct_for_usage(
    request: UsageDeductRequest, 
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # 잔액 확인
    balance = get_balance(request.wallet_address)
    if balance < request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. Available: {balance}, Requested: {request.amount}"
        )
    
    # 사용자 조회
    user = db.query(User).filter(User.wallet_address == request.wallet_address).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 사용량 차감 요청 기록
    tx = Transaction(
        user_wallet=user.wallet_address,
        tx_hash="pending",
        amount=request.amount,
        tx_type="usage_request",
        status="pending"
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    
    return {"message": "Usage deduction request submitted successfully", "request_id": tx.id}

# 사용량 차감 트랜잭션 알림
@router.post("/usage/notify", response_model=TransactionStatusResponse)
def notify_usage_deduction_transaction(
    tx_data: TransactionNotify, 
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    try:
        # 트랜잭션 검증
        verification = verify_usage_deduction_transaction(tx_data.tx_hash)
        
        if verification["success"]:
            # 사용자 조회
            user = db.query(User).filter(User.wallet_address == verification["user"]).first()
            
            if not user:
                return {"status": "failed", "message": "User not found"}
            
            # 트랜잭션 기록
            tx = Transaction(
                user_wallet=user.wallet_address,
                tx_hash=tx_data.tx_hash,
                amount=verification["amount"],
                tx_type="usage_deduction",
                status="confirmed"
            )
            db.add(tx)
            db.commit()
            
            return {"status": "success", "message": "Usage deduction transaction verified and recorded"}
        else:
            return {"status": "failed", "message": verification["message"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
