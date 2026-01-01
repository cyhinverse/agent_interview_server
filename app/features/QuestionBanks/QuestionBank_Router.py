from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.features.QuestionBanks.QuestionBank_Schema import QuestionBankCreate, QuestionBankUpdate, QuestionBankResponse
from app.features.QuestionBanks.QuestionBank_Service import QuestionBankService
from app.features.QuestionBanks.QuestionBank_Dependencies import get_question_bank_service

router = APIRouter(prefix="/question-banks", tags=["Question Banks"])

@router.post("/", response_model=QuestionBankResponse, summary="Create a new question")
async def create_question(
    data: QuestionBankCreate,
    service: QuestionBankService = Depends(get_question_bank_service)
):
    return await service.create_question(data)

@router.get("/", response_model=List[QuestionBankResponse], summary="List questions")
async def list_questions(
    skip: int = 0,
    take: int = 20,
    categoryId: Optional[str] = Query(None, description="Filter by Category ID"),
    service: QuestionBankService = Depends(get_question_bank_service)
):
    return await service.list_questions(skip, take, categoryId)

@router.get("/{question_id}", response_model=QuestionBankResponse, summary="Get question details")
async def get_question(
    question_id: str,
    service: QuestionBankService = Depends(get_question_bank_service)
):
    question = await service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=QuestionBankResponse, summary="Update question")
async def update_question(
    question_id: str,
    data: QuestionBankUpdate,
    service: QuestionBankService = Depends(get_question_bank_service)
):
    question = await service.update_question(question_id, data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.delete("/{question_id}", summary="Delete question")
async def delete_question(
    question_id: str,
    service: QuestionBankService = Depends(get_question_bank_service)
):
    success = await service.delete_question(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}
