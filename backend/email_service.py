import sendgrid
from sendgrid.helpers.mail import Mail
import os
from typing import Dict, Any

class EmailService:
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    
    def forward_email(self, 
                     original_sender: str, 
                     original_subject: str, 
                     original_body: str, 
                     temp_email_address: str,
                     user_main_email: str) -> bool:
        try:
            forwarded_subject = f"[Forwarded from {temp_email_address}] {original_subject}"
            
            forwarded_body = f"""
This email was forwarded from your temporary email address: {temp_email_address}

Original Sender: {original_sender}
Original Subject: {original_subject}

--- Original Message ---
{original_body}

---
This message was automatically forwarded by AI Email Router.
"""
            
            message = Mail(
                from_email=f"noreply@{os.getenv('DOMAIN', 'example.com')}",
                to_emails=user_main_email,
                subject=forwarded_subject,
                html_content=forwarded_body.replace('\n', '<br>')
            )
            
            response = self.sg.send(message)
            return response.status_code in [200, 202]
            
        except Exception as e:
            print(f"Error forwarding email: {str(e)}")
            return False
    
    def send_notification(self, to_email: str, subject: str, body: str) -> bool:
        try:
            message = Mail(
                from_email=f"noreply@{os.getenv('DOMAIN', 'example.com')}",
                to_emails=to_email,
                subject=subject,
                html_content=body
            )
            
            response = self.sg.send(message)
            return response.status_code in [200, 202]
            
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False