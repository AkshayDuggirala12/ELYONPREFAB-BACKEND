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

# The Pure CRM Lead Model
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    site_dimensions = Column(String)
    intended_use = Column(String)
    timeline = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)