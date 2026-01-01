from typing import List, Optional
from app.features.QuestionBanks.QuestionBank_Repository import QuestionBankRepository
from app.features.QuestionBanks.QuestionBank_Schema import QuestionBankCreate, QuestionBankUpdate, QuestionBankResponse

class QuestionBankService:
    def __init__(self, repo: QuestionBankRepository):
        self.repo = repo

    async def create_question(self, data: QuestionBankCreate) -> QuestionBankResponse:
        question = await self.repo.create(data.model_dump())
        return QuestionBankResponse.model_validate(question)

    async def get_question(self, question_id: str) -> Optional[QuestionBankResponse]:
        question = await self.repo.get_by_id(question_id)
        if question:
            return QuestionBankResponse.model_validate(question)
        return None

    async def list_questions(self, skip: int = 0, take: int = 20, category_id: Optional[str] = None) -> List[QuestionBankResponse]:
        if category_id:
            questions = await self.repo.get_by_category(category_id, skip, take)
        else:
            questions = await self.repo.get_all(skip, take)
        return [QuestionBankResponse.model_validate(q) for q in questions]

    async def update_question(self, question_id: str, data: QuestionBankUpdate) -> Optional[QuestionBankResponse]:
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        question = await self.repo.update(question_id, update_data)
        if question:
            return QuestionBankResponse.model_validate(question)
        return None

    async def delete_question(self, question_id: str) -> bool:
        question = await self.repo.delete(question_id)
        return question is not None
