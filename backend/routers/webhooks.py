from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import json
from datetime import datetime

from database import get_db
from models import TempEmail, EmailLog, User, ForwardingRule
from ai_classifier import AIEmailClassifier
from email_service import EmailService

router = APIRouter()

@router.post("/sendgrid")
async def handle_sendgrid_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.body()
        events = json.loads(body.decode('utf-8'))
        
        classifier = AIEmailClassifier()
        email_service = EmailService()
        
        processed_count = 0
        
        for event in events:
            if event.get('event') == 'inbound':
                processed = await process_inbound_email(event, db, classifier, email_service)
                if processed:
                    processed_count += 1
        
        return {"message": f"Processed {processed_count} emails"}
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

async def process_inbound_email(event: dict, db: Session, classifier: AIEmailClassifier, email_service: EmailService):
    try:
        to_email = event.get('to', [{}])[0].get('email', '').lower()
        from_email = event.get('from', '')
        subject = event.get('subject', '')
        text_body = event.get('text', '')
        html_body = event.get('html', '')
        
        body = html_body if html_body else text_body
        
        temp_email = db.query(TempEmail).filter(
            TempEmail.address == to_email,
            TempEmail.is_active == True
        ).first()
        
        if not temp_email:
            return False
        
        if temp_email.expires_at and temp_email.expires_at < datetime.utcnow():
            temp_email.is_active = False
            db.commit()
            return False
        
        user = db.query(User).filter(User.id == temp_email.user_id).first()
        if not user:
            return False
        
        forwarding_rules = db.query(ForwardingRule).filter(
            ForwardingRule.user_id == user.id,
            ForwardingRule.is_active == True
        ).all()
        
        rule_result = classifier.apply_user_rules(from_email, subject, body, forwarding_rules)
        
        if rule_result:
            action = rule_result["action"]
            confidence = rule_result["confidence"]
            reasoning = rule_result["reasoning"]
        else:
            ai_result = classifier.classify_email(from_email, subject, body, temp_email.purpose)
            action = ai_result["action"]
            confidence = ai_result["confidence"]
            reasoning = ai_result["reasoning"]
        
        success = True
        if action == "forward":
            success = email_service.forward_email(
                original_sender=from_email,
                original_subject=subject,
                original_body=body,
                temp_email_address=to_email,
                user_main_email=user.email
            )
        
        email_log = EmailLog(
            temp_email_id=temp_email.id,
            sender_email=from_email,
            subject=subject,
            body_preview=body[:200] if body else "",
            action_taken=action if success else "failed",
            ai_confidence_score=confidence,
            ai_reasoning=reasoning
        )
        
        db.add(email_log)
        db.commit()
        
        return True
        
    except Exception as e:
        print(f"Error processing email: {str(e)}")
        return False