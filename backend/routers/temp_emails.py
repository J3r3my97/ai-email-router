from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import os
from datetime import datetime, timedelta

from database import get_db
from models import User, TempEmail
from schemas import TempEmailCreate, TempEmail as TempEmailSchema
from routers.auth import get_current_user

router = APIRouter()

def generate_temp_email(domain: str) -> str:
    unique_id = str(uuid.uuid4())[:8]
    return f"temp-{unique_id}@{domain}"

@router.post("/", response_model=TempEmailSchema)
def create_temp_email(
    temp_email: TempEmailCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    domain = os.getenv("DOMAIN", "example.com")
    
    max_attempts = 10
    for _ in range(max_attempts):
        address = generate_temp_email(domain)
        existing = db.query(TempEmail).filter(TempEmail.address == address).first()
        if not existing:
            break
    else:
        raise HTTPException(status_code=500, detail="Could not generate unique email address")
    
    if temp_email.expires_at is None:
        temp_email.expires_at = datetime.utcnow() + timedelta(days=30)
    
    db_temp_email = TempEmail(
        user_id=current_user.id,
        address=address,
        purpose=temp_email.purpose,
        expires_at=temp_email.expires_at
    )
    
    db.add(db_temp_email)
    db.commit()
    db.refresh(db_temp_email)
    return db_temp_email

@router.get("/", response_model=List[TempEmailSchema])
def list_temp_emails(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(TempEmail).filter(TempEmail.user_id == current_user.id).all()

@router.get("/{temp_email_id}", response_model=TempEmailSchema)
def get_temp_email(
    temp_email_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    temp_email = db.query(TempEmail).filter(
        TempEmail.id == temp_email_id,
        TempEmail.user_id == current_user.id
    ).first()
    
    if not temp_email:
        raise HTTPException(status_code=404, detail="Temp email not found")
    
    return temp_email

@router.delete("/{temp_email_id}")
def deactivate_temp_email(
    temp_email_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    temp_email = db.query(TempEmail).filter(
        TempEmail.id == temp_email_id,
        TempEmail.user_id == current_user.id
    ).first()
    
    if not temp_email:
        raise HTTPException(status_code=404, detail="Temp email not found")
    
    temp_email.is_active = False
    db.commit()
    
    return {"message": "Temp email deactivated successfully"}