from fastapi import Depends
from app.features.QuestionBanks.QuestionBank_Repository import QuestionBankRepository
from app.features.QuestionBanks.QuestionBank_Service import QuestionBankService

def get_question_bank_repository() -> QuestionBankRepository:
    return QuestionBankRepository()

def get_question_bank_service(
    repo: QuestionBankRepository = Depends(get_question_bank_repository)
) -> QuestionBankService:
    return QuestionBankService(repo)
