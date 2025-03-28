from pydantic import BaseModel, Field
from typing import Optional

class NonceRequest(BaseModel):
    wallet_address: str = Field(..., description="User's blockchain wallet address")

class NonceResponse(BaseModel):
    wallet_address: str
    nonce: str
    message: str = Field(..., description="Message to be signed by the wallet")

class VerifySignatureRequest(BaseModel):
    wallet_address: str = Field(..., description="User's blockchain wallet address")
    signature: str = Field(..., description="Signature of the nonce message")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    wallet_address: str
    token_balance: float = 0.0
