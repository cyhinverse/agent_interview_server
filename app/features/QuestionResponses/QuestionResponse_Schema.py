from pydantic import BaseModel
from typing import Optional

class QuestionResponseBase(BaseModel):
    sessionId: str
    questionId: str
    answer: str
    score: float
    comment: Optional[str] = None

class QuestionResponseCreate(QuestionResponseBase):
    pass

class QuestionResponseUpdate(BaseModel):
    answer: Optional[str] = None
    score: Optional[float] = None
    comment: Optional[str] = None

class QuestionResponseResponse(QuestionResponseBase):
    id: str

    class Config:
        from_attributes = True
