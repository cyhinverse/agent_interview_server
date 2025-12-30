from typing import List, Optional
from prisma.models import InterviewCategory
from app.shared.database import db
from app.features.InterviewCategorys.InterviewCategory_Schema import InterviewCategoryCreate, InterviewCategoryUpdate

class InterviewCategoryRepository:
    # -------------------------------------------------------------------------
    # Repository for handling Interview Category-related database operations.
    # -------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------
    # Create a new interview category.
    #
    # Args:
    #     data (InterviewCategoryCreate): The data for the new category.
    #
    # Returns:
    #     InterviewCategory: The created category object.
    # -------------------------------------------------------------------------
    async def create(self, data: InterviewCategoryCreate) -> InterviewCategory:
        return await db.interviewcategory.create(data=data.model_dump())

    # -------------------------------------------------------------------------
    # Retrieve all interview categories with pagination.
    #
    # Args:
    #     skip (int): Number of records to skip.
    #     take (int): Number of records to return.
    #
    # Returns:
    #     List[InterviewCategory]: A list of categories.
    # -------------------------------------------------------------------------
    async def get_all(self, skip: int = 0, take: int = 100) -> List[InterviewCategory]:
        return await db.interviewcategory.find_many(skip=skip, take=take, order={"createdAt": "desc"})

    # -------------------------------------------------------------------------
    # Retrieve a category by its ID.
    #
    # Args:
    #     category_id (str): The unique UUID of the category.
    #
    # Returns:
    #     Optional[InterviewCategory]: The category object, or None if not found.
    # -------------------------------------------------------------------------
    async def get_by_id(self, category_id: str) -> Optional[InterviewCategory]:
        return await db.interviewcategory.find_unique(where={"id": category_id})

    # -------------------------------------------------------------------------
    # Retrieve a category by its unique slug.
    #
    # Args:
    #     slug (str): The unique slug string.
    #
    # Returns:
    #     Optional[InterviewCategory]: The category object, or None if not found.
    # -------------------------------------------------------------------------
    async def get_by_slug(self, slug: str) -> Optional[InterviewCategory]:
        return await db.interviewcategory.find_unique(where={"slug": slug})

    # -------------------------------------------------------------------------
    # Update an existing category.
    #
    # Args:
    #     category_id (str): The UUID of the category to update.
    #     data (InterviewCategoryUpdate): The data fields to update.
    #
    # Returns:
    #     Optional[InterviewCategory]: The updated category object.
    # -------------------------------------------------------------------------
    async def update(self, category_id: str, data: InterviewCategoryUpdate) -> Optional[InterviewCategory]:
        update_data = data.model_dump(exclude_unset=True)
        return await db.interviewcategory.update(where={"id": category_id}, data=update_data)

    # -------------------------------------------------------------------------
    # Delete a category by its ID.
    #
    # Args:
    #     category_id (str): The UUID of the category to delete.
    #
    # Returns:
    #     Optional[InterviewCategory]: The deleted category object.
    # -------------------------------------------------------------------------
    async def delete(self, category_id: str) -> Optional[InterviewCategory]:
        return await db.interviewcategory.delete(where={"id": category_id})