from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    wallet_address = Column(String, unique=True, index=True)
    balance = Column(Integer, default=0)  # 잔액은 블록체인에서 조회하므로 참조용
    is_admin = Column(Boolean, default=False)  # 관리자 여부
    nonce = Column(String, nullable=True)  # 인증에 사용되는 nonce
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    transactions = relationship("Transaction", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tx_hash = Column(String, unique=True, index=True)
    amount = Column(Integer)  # wei 단위
    tx_type = Column(String)  # deposit, withdraw, withdraw_request, usage_request, usage_deduction
    status = Column(String)  # pending, confirmed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transactions")

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_id = Column(String, unique=True, index=True, nullable=False)  # Public identifier
    secret_key_hash = Column(String, nullable=False)  # Hashed secret key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)  # Optional name for the API key
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Usage tracking
    call_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    rate_limit_per_minute = Column(Integer, default=60)  # Default rate limit
    
    # Token consumption
    token_consumption_rate = Column(Float, default=0.01)  # Tokens consumed per API call
    
    # Relationship
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey key_id={self.key_id} user_id={self.user_id}>"
