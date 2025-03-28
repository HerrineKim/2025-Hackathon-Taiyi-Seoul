from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DepositTransactionBase(BaseModel):
    transaction_hash: str = Field(..., description="Blockchain transaction hash")
    amount: float = Field(..., description="Amount of tokens deposited")

class DepositTransactionCreate(DepositTransactionBase):
    pass

class DepositTransactionResponse(DepositTransactionBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True
