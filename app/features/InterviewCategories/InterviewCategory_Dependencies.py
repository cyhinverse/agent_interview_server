from fastapi import Depends
from app.features.InterviewCategories.InterviewCategory_Repository import InterviewCategoryRepository
from app.features.InterviewCategories.InterviewCategory_Service import InterviewCategoryService

def get_interview_category_repository() -> InterviewCategoryRepository:
    return InterviewCategoryRepository()

def get_interview_category_service(repo: InterviewCategoryRepository = Depends(get_interview_category_repository)) -> InterviewCategoryService:
    return InterviewCategoryService(repo)
