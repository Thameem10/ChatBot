from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    name: str
    email: str
    role: str


class AdminCreate(AdminBase):
    password: str
    refreshToken: Optional[str] = None


class AdminLogin(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refreshToken: str

class AdminDetails(BaseModel):
    adminId: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True  

class AdminResponse(AdminBase):
    adminId: int
    refreshToken: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
