from fastapi import Depends
from app.features.InterviewSessions.InterviewSession_Repository import InterviewSessionRepository
from app.features.InterviewSessions.InterviewSession_Service import InterviewSessionService
from app.features.InterviewCategorys.InterviewCategory_Dependencies import get_interview_category_repository
from app.features.InterviewCategorys.InterviewCategory_Repository import InterviewCategoryRepository

def get_interview_session_repository() -> InterviewSessionRepository:
    return InterviewSessionRepository()

def get_interview_session_service(
    repo: InterviewSessionRepository = Depends(get_interview_session_repository),
    category_repo: InterviewCategoryRepository = Depends(get_interview_category_repository)
) -> InterviewSessionService:
    return InterviewSessionService(repo, category_repo)
