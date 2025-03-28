from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base

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
