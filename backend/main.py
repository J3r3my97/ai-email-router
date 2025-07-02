from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from database import engine, get_db
from models import Base
from routers import auth, temp_emails, webhooks, dashboard

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Email Router",
    description="A platform for temporary email addresses with AI-powered filtering",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(temp_emails.router, prefix="/api/temp-emails", tags=["temp-emails"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "AI Email Router API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )