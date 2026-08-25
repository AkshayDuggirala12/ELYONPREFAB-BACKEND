from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
import datetime

# Matches the "Products" section (PEB, LGSF, Modular)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    image_url = Column(String)

# Matches the "Recent Projects" portfolio section
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    location = Column(String)
    duration = Column(String) # e.g., "6 WKS"
    image_url = Column(String)
    # ... your existing columns (title, location, duration, image_url)
    video_url = Column(String, nullable=True)  # New!
    description = Column(String, nullable=True) # New!

# Matches the "Need a custom solution?" and "Get a Quote" forms
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    project_type = Column(String) # e.g., "Warehouse", "Labour Accommodation"
    dimensions = Column(String)
    timeline = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)