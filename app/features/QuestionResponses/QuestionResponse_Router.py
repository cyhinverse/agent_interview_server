from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.features.QuestionResponses.QuestionResponse_Schema import QuestionResponseCreate, QuestionResponseUpdate, QuestionResponseResponse
from app.features.QuestionResponses.QuestionResponse_Service import QuestionResponseService
from app.features.QuestionResponses.QuestionResponse_Dependencies import get_question_response_service

router = APIRouter(prefix="/question-responses", tags=["Question Responses"])

@router.post("/", response_model=QuestionResponseResponse, summary="Submit a response to a question")
async def create_response(
    data: QuestionResponseCreate,
    service: QuestionResponseService = Depends(get_question_response_service)
):
    return await service.create_response(data)

@router.get("/session/{session_id}", response_model=List[QuestionResponseResponse], summary="List responses for a session")
async def list_responses_by_session(
    session_id: str,
    skip: int = 0,
    take: int = 20,
    service: QuestionResponseService = Depends(get_question_response_service)
):
    return await service.list_responses_by_session(session_id, skip, take)

@router.get("/{response_id}", response_model=QuestionResponseResponse, summary="Get response details")
async def get_response(
    response_id: str,
    service: QuestionResponseService = Depends(get_question_response_service)
):
    response = await service.get_response(response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response

@router.put("/{response_id}", response_model=QuestionResponseResponse, summary="Update response")
async def update_response(
    response_id: str,
    data: QuestionResponseUpdate,
    service: QuestionResponseService = Depends(get_question_response_service)
):
    response = await service.update_response(response_id, data)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response

@router.delete("/{response_id}", summary="Delete response")
async def delete_response(
    response_id: str,
    service: QuestionResponseService = Depends(get_question_response_service)
):
    success = await service.delete_response(response_id)
    if not success:
        raise HTTPException(status_code=404, detail="Response not found")
    return {"message": "Response deleted successfully"}
