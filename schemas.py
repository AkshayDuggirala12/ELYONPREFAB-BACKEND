from pydantic import BaseModel
from typing import Optional

# What React needs to send when someone submits a lead form
class LeadCreate(BaseModel):
    name: str
    phone: str
    site_dimensions: Optional[str] = None
    intended_use: Optional[str] = None
    timeline: Optional[str] = None
    message: Optional[str] = None