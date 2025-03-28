from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class APIKeyCreate(BaseModel):
    name: Optional[str] = Field(None, description="Optional name for the API key")
    rate_limit_per_minute: Optional[int] = Field(60, description="Rate limit per minute")

class APIKeyResponse(BaseModel):
    key_id: str
    name: Optional[str]
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]
    rate_limit_per_minute: int
    
    class Config:
        orm_mode = True

class APIKeyWithSecret(APIKeyResponse):
    secret_key: str = Field(..., description="Secret key (only shown once)")

class APIKeyUsage(APIKeyResponse):
    call_count: int
    last_used_at: Optional[datetime]
    token_consumption_rate: float
    
    class Config:
        orm_mode = True
