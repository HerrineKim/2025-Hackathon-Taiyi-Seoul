from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, index=True, nullable=False)
    nonce = Column(String, nullable=False)  # For wallet authentication
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Token deposit information
    token_balance = Column(Float, default=0.0)  # Current token balance
    deposit_contract_address = Column(String, nullable=True)  # Smart contract address for deposits
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User wallet_address={self.wallet_address}>"
