import openai
import os
from typing import Dict, Any
import re
from datetime import datetime

class AIEmailClassifier:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def classify_email(self, sender_email: str, subject: str, body: str, temp_email_purpose: str = None) -> Dict[str, Any]:
        try:
            prompt = self._build_classification_prompt(sender_email, subject, body, temp_email_purpose)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that classifies emails as important or junk. Respond with a JSON object containing 'action' (forward/delete), 'confidence' (0-1), and 'reasoning'."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            result = self._parse_ai_response(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "action": "forward",
                "confidence": 0.5,
                "reasoning": f"AI classification failed: {str(e)}. Defaulting to forward for safety."
            }
    
    def _build_classification_prompt(self, sender_email: str, subject: str, body: str, temp_email_purpose: str = None) -> str:
        prompt = f"""Classify this email as either important (should be forwarded) or junk (should be deleted).

Context:
- This email was sent to a temporary email address
- Purpose of temp email: {temp_email_purpose or 'Not specified'}

Email Details:
From: {sender_email}
Subject: {subject}
Body: {body[:500]}...

Classification Criteria:
FORWARD if:
- Account verification/confirmation emails
- Order confirmations or shipping notifications
- Important service updates or security alerts
- Event tickets or confirmations
- Password reset requests
- Payment receipts

DELETE if:
- Marketing/promotional emails
- Newsletters
- Spam or suspicious content
- Unrelated promotional offers
- Generic advertising

Respond with JSON format:
{{"action": "forward" or "delete", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}"""
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        try:
            import json
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        if "forward" in response_text.lower():
            action = "forward"
        elif "delete" in response_text.lower():
            action = "delete"
        else:
            action = "forward"
        
        confidence_match = re.search(r'(\d+\.?\d*)%?', response_text)
        confidence = float(confidence_match.group(1)) / 100 if confidence_match else 0.7
        
        return {
            "action": action,
            "confidence": min(confidence, 1.0),
            "reasoning": response_text[:200]
        }
    
    def apply_user_rules(self, sender_email: str, subject: str, body: str, forwarding_rules: list) -> Dict[str, Any]:
        for rule in forwarding_rules:
            if not rule.is_active:
                continue
                
            keywords = [kw.strip().lower() for kw in rule.keywords.split(',')]
            content_to_check = f"{sender_email} {subject} {body}".lower()
            
            if any(keyword in content_to_check for keyword in keywords):
                return {
                    "action": rule.action,
                    "confidence": 1.0,
                    "reasoning": f"Matched user rule: {rule.keywords}"
                }
        
        return None