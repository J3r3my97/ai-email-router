from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    temp_emails = relationship("TempEmail", back_populates="user")
    forwarding_rules = relationship("ForwardingRule", back_populates="user")

class TempEmail(Base):
    __tablename__ = "temp_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address = Column(String, unique=True, index=True, nullable=False)
    purpose = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="temp_emails")
    email_logs = relationship("EmailLog", back_populates="temp_email")

class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    temp_email_id = Column(Integer, ForeignKey("temp_emails.id"), nullable=False)
    sender_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body_preview = Column(Text, nullable=True)
    action_taken = Column(String, nullable=False)  # 'forwarded', 'deleted', 'quarantined'
    ai_confidence_score = Column(Float, nullable=True)
    ai_reasoning = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    temp_email = relationship("TempEmail", back_populates="email_logs")

class ForwardingRule(Base):
    __tablename__ = "forwarding_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    keywords = Column(String, nullable=False)
    action = Column(String, nullable=False)  # 'forward', 'delete', 'quarantine'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="forwarding_rules")