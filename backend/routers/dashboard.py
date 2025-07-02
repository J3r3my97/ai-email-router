from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List

from database import get_db
from models import User, TempEmail, EmailLog
from schemas import DashboardStats, EmailLog as EmailLogSchema
from routers.auth import get_current_user

router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_temp_emails = db.query(TempEmail).filter(
        TempEmail.user_id == current_user.id
    ).count()
    
    active_temp_emails = db.query(TempEmail).filter(
        TempEmail.user_id == current_user.id,
        TempEmail.is_active == True
    ).count()
    
    emails_forwarded = db.query(func.count(EmailLog.id)).join(TempEmail).filter(
        TempEmail.user_id == current_user.id,
        EmailLog.action_taken == "forward"
    ).scalar()
    
    emails_deleted = db.query(func.count(EmailLog.id)).join(TempEmail).filter(
        TempEmail.user_id == current_user.id,
        EmailLog.action_taken == "delete"
    ).scalar()
    
    recent_activity = db.query(EmailLog).join(TempEmail).filter(
        TempEmail.user_id == current_user.id
    ).order_by(desc(EmailLog.created_at)).limit(10).all()
    
    return DashboardStats(
        total_temp_emails=total_temp_emails,
        active_temp_emails=active_temp_emails,
        emails_forwarded=emails_forwarded or 0,
        emails_deleted=emails_deleted or 0,
        recent_activity=recent_activity
    )

@router.get("/emails", response_model=List[EmailLogSchema])
def get_email_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    return db.query(EmailLog).join(TempEmail).filter(
        TempEmail.user_id == current_user.id
    ).order_by(desc(EmailLog.created_at)).limit(limit).all()