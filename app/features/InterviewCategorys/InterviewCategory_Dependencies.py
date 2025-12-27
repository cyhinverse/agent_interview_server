from fastapi import Depends
from app.features.interviews.interview_repository import InterviewRepository
from app.features.interviews.interview_service import InterviewService


def get_interview_repository() -> InterviewRepository:
    return InterviewRepository()

def get_interview_service(repo: InterviewRepository = Depends(get_interview_repository)) -> InterviewService:
    return InterviewService(repo)

