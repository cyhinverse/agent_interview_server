from fastapi import APIRouter, Depends
from typing import List
from app.features.InterviewCategorys.InterviewCategory_Schema import InterviewCategoryCreate, InterviewCategoryUpdate, InterviewCategoryResponse
from app.features.InterviewCategorys.InterviewCategory_Service import InterviewCategoryService
from app.features.InterviewCategorys.InterviewCategory_Dependencies import get_interview_category_service

router = APIRouter(prefix="/interview-categories", tags=["Interview Categories"])

# -------------------------------------------------------------------------
# Create a new interview category.
#
# - **name**: Name of the category.
# - **slug**: Unique URL-friendly identifier.
# - **systemPrompt**: System prompt for AI context.
# - **language**: Language code (default: vi-VN).
# -------------------------------------------------------------------------
@router.post("/", response_model=InterviewCategoryResponse, summary="Create new category")
async def create_category(
    data: InterviewCategoryCreate,
    service: InterviewCategoryService = Depends(get_interview_category_service)
):
    return await service.create_category(data)

# -------------------------------------------------------------------------
# Retrieve a list of all available interview categories.
# -------------------------------------------------------------------------
@router.get("/", response_model=List[InterviewCategoryResponse], summary="List all categories")
async def list_categories(
    service: InterviewCategoryService = Depends(get_interview_category_service)
):
    return await service.get_all_categories()

# -------------------------------------------------------------------------
# Retrieve details of a specific interview category by its ID.
# -------------------------------------------------------------------------
@router.get("/{category_id}", response_model=InterviewCategoryResponse, summary="Get category by ID")
async def get_category(
    category_id: str,
    service: InterviewCategoryService = Depends(get_interview_category_service)
):
    return await service.get_category_by_id(category_id)

# -------------------------------------------------------------------------
# Update an existing interview category.
#
# Only provided fields will be updated.
# -------------------------------------------------------------------------
@router.put("/{category_id}", response_model=InterviewCategoryResponse, summary="Update category")
async def update_category(
    category_id: str,
    data: InterviewCategoryUpdate,
    service: InterviewCategoryService = Depends(get_interview_category_service)
):
    return await service.update_category(category_id, data)

# -------------------------------------------------------------------------
# Permanently delete an interview category.
# -------------------------------------------------------------------------
@router.delete("/{category_id}", summary="Delete category")
async def delete_category(
    category_id: str,
    service: InterviewCategoryService = Depends(get_interview_category_service)
):
    await service.delete_category(category_id)
    return {"message": "Category deleted successfully"}