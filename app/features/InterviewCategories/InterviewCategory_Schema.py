from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InterviewCategoryBase(BaseModel):
    name: str
    slug: str
    systemPrompt: str
    language: Optional[str] = "vi-VN"

class InterviewCategoryCreate(InterviewCategoryBase):
    pass

class InterviewCategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    systemPrompt: Optional[str] = None
    language: Optional[str] = None

class InterviewCategoryResponse(InterviewCategoryBase):
    id: str
    createdAt: datetime

    class Config:
        from_attributes = True