from fastapi import Depends
from app.features.QuestionResponses.QuestionResponse_Repository import QuestionResponseRepository
from app.features.QuestionResponses.QuestionResponse_Service import QuestionResponseService
from app.features.QuestionBanks.QuestionBank_Dependencies import get_question_bank_repository
from app.features.QuestionBanks.QuestionBank_Repository import QuestionBankRepository

def get_question_response_repository() -> QuestionResponseRepository:
    return QuestionResponseRepository()

def get_question_response_service(
    repo: QuestionResponseRepository = Depends(get_question_response_repository),
    question_repo: QuestionBankRepository = Depends(get_question_bank_repository)
) -> QuestionResponseService:
    return QuestionResponseService(repo, question_repo)
