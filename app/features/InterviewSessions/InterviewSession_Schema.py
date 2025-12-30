from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.features.InterviewCategorys.InterviewCategory_Schema import InterviewCategoryResponse
from app.features.Users.User_Schemas import UserResponse

class InterviewSessionBase(BaseModel):
    categoryId: str

class InterviewSessionCreate(InterviewSessionBase):
    pass

class InterviewSessionUpdate(BaseModel):
    status: Optional[str] = None
    endTime: Optional[datetime] = None

class InterviewSessionResponse(BaseModel):
    id: str
    userId: str
    categoryId: str
    dailyRoomUrl: str
    status: str
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    createdAt: datetime
    
    # Optional relations if we want to embed them
    user: Optional[UserResponse] = None
    category: Optional[InterviewCategoryResponse] = None

    class Config:
        from_attributes = True
