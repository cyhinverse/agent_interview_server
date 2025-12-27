from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    fullName: str
    email: EmailStr
    password: str
    avatarUrl: Optional[str] = None

class UserUpdate(BaseModel):
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
    avatarUrl: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    fullName: str
    email: EmailStr
    avatarUrl: Optional[str] = None
    role: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
