from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    wallet_address: str = Field(..., description="User's blockchain wallet address")

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool
    token_balance: float
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserWithBalance(UserResponse):
    token_balance: float
    deposit_contract_address: Optional[str] = None
    
    class Config:
        orm_mode = True
