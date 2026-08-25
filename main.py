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


# This automatically creates the tables in your elyon_db!
models.Base.metadata.drop_all(bind=engine)   # ADD THIS LINE TO WIPE IT
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

# --- ROUTES ---

@app.get("/")
def read_root():
    return {"message": "Elyon Prefab Backend is Live!"}

# Get all portfolio projects
@app.get("/api/projects/")
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

# Create a schema for the new project
class ProjectCreate(BaseModel):
    title: str
    location: str
    duration: str
    image_url: str
    video_url: str = None
    description: str = None

# Securely add a new project
@app.post("/api/projects/")
def create_project(project: ProjectCreate, authorization: str = Header(default=None), db: Session = Depends(get_db)):
    # Check security token
    SECRET_TOKEN = os.getenv("SECRET_TOKEN")
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized Access")

    # Save to PostgreSQL
    new_project = models.Project(
        title=project.title,
        location=project.location,
        duration=project.duration,
        image_url=project.image_url,
        video_url=project.video_url,
        description=project.description
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"status": "success", "project_id": new_project.id}

# Get all products
@app.get("/api/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

class AdminLogin(BaseModel):
    phone: str
    password: str

@app.post("/api/admin/login")
def admin_login(req: AdminLogin):
    # Now grabbing the secure info from the hidden .env file!
    ADMIN_PHONE = os.getenv("ADMIN_PHONE")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    SECRET_TOKEN = os.getenv("SECRET_TOKEN")

    if req.phone == ADMIN_PHONE and req.password == ADMIN_PASSWORD:
        return {"status": "success", "token": SECRET_TOKEN}
    else:
        raise HTTPException(status_code=401, detail="Invalid phone or password")

# Submit a new lead/quote request
@app.post("/api/leads/")
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    # Convert the Pydantic schema into a SQLAlchemy model
    db_lead = models.Lead(**lead.model_dump())
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    return {"status": "success", "message": "Quote request received!", "lead_id": db_lead.id}

# Get all leads (Now highly secured!)
@app.get("/api/leads/")
def get_all_leads(authorization: str = Header(default=None), db: Session = Depends(get_db)):
    SECRET_TOKEN = os.getenv("SECRET_TOKEN")

    # Check if the token is missing or incorrect
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized Access")

    # .order_by(models.Lead.id.desc()) puts the newest leads at the top!
    return db.query(models.Lead).order_by(models.Lead.id.desc()).all()