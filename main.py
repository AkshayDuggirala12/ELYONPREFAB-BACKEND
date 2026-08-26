from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Keep this safe! No drop_all here.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Elyon Prefab API")

# Allow React to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Elyon Prefab Backend is Live!"}

# --- AUTHENTICATION ---
class AdminLogin(BaseModel):
    phone: str
    password: str

@app.post("/api/admin/login")
def admin_login(req: AdminLogin):
    ADMIN_PHONE = os.getenv("ADMIN_PHONE")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    SECRET_TOKEN = os.getenv("SECRET_TOKEN")

    if req.phone == ADMIN_PHONE and req.password == ADMIN_PASSWORD:
        return {"status": "success", "token": SECRET_TOKEN}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# --- CRM LEADS ---
@app.post("/api/leads/")
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = models.Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return {"status": "success", "message": "Quote request received!", "lead_id": db_lead.id}

@app.get("/api/leads/")
def get_all_leads(authorization: str = Header(default=None), db: Session = Depends(get_db)):
    SECRET_TOKEN = os.getenv("SECRET_TOKEN")
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    
    # Newest leads at the top
    return db.query(models.Lead).order_by(models.Lead.id.desc()).all()