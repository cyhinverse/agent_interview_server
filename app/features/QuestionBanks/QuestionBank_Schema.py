from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
# Assuming we might want to include Category info in response, but let's keep it simple for now or use forward ref if needed.

class QuestionBankBase(BaseModel):
    categoryId: str
    questionText: str
    expectedAnswer: str
    difficulty: Optional[str] = None

class QuestionBankCreate(QuestionBankBase):
    pass

class QuestionBankUpdate(BaseModel):
    categoryId: Optional[str] = None
    questionText: Optional[str] = None
    expectedAnswer: Optional[str] = None
    difficulty: Optional[str] = None

class QuestionBankResponse(BaseModel):
    id: str
    categoryId: str
    questionText: str
    expectedAnswer: str
    difficulty: Optional[str] = None
    # We can add 'category' relation if needed later

    class Config:
        from_attributes = True
