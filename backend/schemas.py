from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TempEmailBase(BaseModel):
    purpose: Optional[str] = None
    expires_at: Optional[datetime] = None

class TempEmailCreate(TempEmailBase):
    pass

class TempEmail(TempEmailBase):
    id: int
    address: str
    user_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class EmailLogBase(BaseModel):
    sender_email: str
    subject: str
    body_preview: Optional[str] = None
    action_taken: str
    ai_confidence_score: Optional[float] = None
    ai_reasoning: Optional[str] = None

class EmailLog(EmailLogBase):
    id: int
    temp_email_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ForwardingRuleBase(BaseModel):
    keywords: str
    action: str

class ForwardingRuleCreate(ForwardingRuleBase):
    pass

class ForwardingRule(ForwardingRuleBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class WebhookEmail(BaseModel):
    to: List[str]
    from_email: str
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None

class DashboardStats(BaseModel):
    total_temp_emails: int
    active_temp_emails: int
    emails_forwarded: int
    emails_deleted: int
    recent_activity: List[EmailLog]