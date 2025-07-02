# AI Email Router MVP

## Project Overview
A platform that provides temporary email addresses with AI-powered filtering to forward only important emails to users' main accounts, preventing spam accumulation from temporary registrations.

## Core Concept
Users create temporary email addresses for services like:
- Free trials
- Concert tickets
- One-time registrations
- Shopping accounts

The AI assistant analyzes incoming emails and only forwards genuinely important messages to the user's main email account, automatically deleting junk mail.

## Tech Stack
- **Backend**: Python (FastAPI recommended)
- **Frontend**: Node.js (React/Next.js recommended)
- **Email Service**: SendGrid integration
- **Database**: PostgreSQL or SQLite for MVP
- **AI/ML**: OpenAI API or local NLP models
- **Domain**: User's own domain for email addresses

## MVP Features

### Core Features
1. **Temporary Email Generation**
   - Create unique email addresses (e.g., user123@yourdomain.com)
   - Set expiration dates for temp addresses
   - Generate memorable or random aliases

2. **AI Email Classification**
   - Analyze incoming email content
   - Classify as "important" vs "junk"
   - Consider context of the temp email's purpose

3. **Email Routing**
   - Forward important emails to user's main account
   - Delete junk emails automatically
   - Maintain logs of actions taken

4. **Web Dashboard**
   - Create/manage temporary email addresses
   - View forwarded emails
   - Review AI decisions and provide feedback
   - Configure forwarding rules

### Technical Architecture
```
[Incoming Email] → [SendGrid Webhook] → [Python Backend] → [AI Classification] → [Forward/Delete]
                                     ↓
[Web Dashboard] ← [Database] ← [Logging & Analytics]
```

## Development Commands
```bash
# Backend (Python)
cd backend
pip install -r requirements.txt
python main.py

# Frontend (Node.js)
cd frontend
npm install
npm run dev

# Run tests
python -m pytest  # Backend tests
npm test          # Frontend tests
```

## Environment Variables
```
SENDGRID_API_KEY=your_sendgrid_key
OPENAI_API_KEY=your_openai_key
DATABASE_URL=your_database_url
DOMAIN=your_domain.com
SECRET_KEY=your_secret_key
```

## Database Schema (Initial)
- **users**: id, email, created_at
- **temp_emails**: id, user_id, address, purpose, expires_at, active
- **email_logs**: id, temp_email_id, subject, sender, action, ai_score, created_at
- **forwarding_rules**: id, user_id, keywords, action

## AI Classification Strategy
1. **Context Awareness**: Consider the purpose of the temp email
2. **Sender Reputation**: Check if sender is legitimate service
3. **Content Analysis**: Analyze subject line and body
4. **User Feedback**: Learn from user corrections
5. **Common Patterns**: Identify promotional vs transactional emails

## MVP Limitations
- Single user (personal use)
- Basic AI classification
- Simple web interface
- Manual SendGrid webhook setup
- No advanced security features

## Future Enhancements
- Multi-user support
- Advanced AI models
- Mobile app
- Bulk email management
- Integration with popular email providers
- API for third-party integrations

## Security Considerations
- Encrypt sensitive data
- Secure webhook endpoints
- Rate limiting
- Email content privacy
- User authentication

## Testing Strategy
- Unit tests for AI classification
- Integration tests for email flow
- Manual testing with real emails
- Performance testing with email volume

## Deployment
- Docker containers for easy deployment
- Environment-based configuration
- Webhook endpoint security
- Domain configuration for email routing