from typing import List, Optional
from app.features.QuestionResponses.QuestionResponse_Repository import QuestionResponseRepository
from app.features.QuestionResponses.QuestionResponse_Schema import QuestionResponseCreate, QuestionResponseUpdate, QuestionResponseResponse
from app.features.QuestionBanks.QuestionBank_Repository import QuestionBankRepository

class QuestionResponseService:
    def __init__(self, repo: QuestionResponseRepository, question_repo: QuestionBankRepository):
        self.repo = repo
        self.question_repo = question_repo

    async def create_response(self, data: QuestionResponseCreate) -> QuestionResponseResponse:
        # Optionally verify question exists or session exists, but FK constraint handles it usually.
        # We might want to auto-calculate score or something here later? For now just CRUD.
        response = await self.repo.create(data.model_dump())
        return QuestionResponseResponse.model_validate(response)

    async def get_response(self, response_id: str) -> Optional[QuestionResponseResponse]:
        response = await self.repo.get_by_id(response_id)
        if response:
            return QuestionResponseResponse.model_validate(response)
        return None

    async def list_responses_by_session(self, session_id: str, skip: int = 0, take: int = 20) -> List[QuestionResponseResponse]:
        responses = await self.repo.get_by_session(session_id, skip, take)
        return [QuestionResponseResponse.model_validate(r) for r in responses]

    async def update_response(self, response_id: str, data: QuestionResponseUpdate) -> Optional[QuestionResponseResponse]:
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        response = await self.repo.update(response_id, update_data)
        if response:
            return QuestionResponseResponse.model_validate(response)
        return None

    async def delete_response(self, response_id: str) -> bool:
        response = await self.repo.delete(response_id)
        return response is not None
