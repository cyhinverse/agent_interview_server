from typing import List
from app.features.InterviewCategorys.InterviewCategory_Repository import InterviewCategoryRepository
from app.features.InterviewCategorys.InterviewCategory_Schema import InterviewCategoryCreate, InterviewCategoryUpdate, InterviewCategoryResponse
from app.shared.exceptions import DuplicatedEntityException, NotFoundException

class InterviewCategoryService:
    # -------------------------------------------------------------------------
    # Service class responsible for business logic related to Interview Categories.
    # -------------------------------------------------------------------------

    def __init__(self, repo: InterviewCategoryRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # Create a new interview category.
    #
    # Checks for slug uniqueness before creating.
    #
    # Args:
    #     data (InterviewCategoryCreate): Data for the new category.
    #
    # Returns:
    #     InterviewCategoryResponse: The created category details.
    #
    # Raises:
    #     DuplicatedEntityException: If the slug already exists.
    # -------------------------------------------------------------------------
    async def create_category(self, data: InterviewCategoryCreate) -> InterviewCategoryResponse:
        existing = await self.repo.get_by_slug(data.slug)
        if existing:
            raise DuplicatedEntityException("Category with this slug already exists")
        
        category = await self.repo.create(data)
        return InterviewCategoryResponse.model_validate(category)

    # -------------------------------------------------------------------------
    # Retrieve all interview categories.
    #
    # Returns:
    #     List[InterviewCategoryResponse]: List of all categories.
    # -------------------------------------------------------------------------
    async def get_all_categories(self) -> List[InterviewCategoryResponse]:
        categories = await self.repo.get_all()
        return [InterviewCategoryResponse.model_validate(c) for c in categories]

    # -------------------------------------------------------------------------
    # Retrieve a category by its ID.
    #
    # Args:
    #     category_id (str): The unique ID of the category.
    #
    # Returns:
    #     InterviewCategoryResponse: The category details.
    #
    # Raises:
    #     NotFoundException: If the category does not exist.
    # -------------------------------------------------------------------------
    async def get_category_by_id(self, category_id: str) -> InterviewCategoryResponse:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundException("Category not found")
        return InterviewCategoryResponse.model_validate(category)

    # -------------------------------------------------------------------------
    # Retrieve a category by its slug.
    #
    # Args:
    #     slug (str): The unique slug of the category.
    #
    # Returns:
    #     InterviewCategoryResponse: The category details.
    #
    # Raises:
    #     NotFoundException: If the category does not exist.
    # -------------------------------------------------------------------------
    async def get_category_by_slug(self, slug: str) -> InterviewCategoryResponse:
        category = await self.repo.get_by_slug(slug)
        if not category:
            raise NotFoundException("Category not found")
        return InterviewCategoryResponse.model_validate(category)

    # -------------------------------------------------------------------------
    # Update an existing category.
    #
    # Args:
    #     category_id (str): The ID of the category to update.
    #     data (InterviewCategoryUpdate): The fields to update.
    #
    # Returns:
    #     InterviewCategoryResponse: The updated category details.
    #
    # Raises:
    #     NotFoundException: If the category does not exist.
    # -------------------------------------------------------------------------
    async def update_category(self, category_id: str, data: InterviewCategoryUpdate) -> InterviewCategoryResponse:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundException("Category not found")
            
        updated_category = await self.repo.update(category_id, data)
        return InterviewCategoryResponse.model_validate(updated_category)

    # -------------------------------------------------------------------------
    # Delete a category by ID.
    #
    # Args:
    #     category_id (str): The ID of the category to delete.
    #
    # Returns:
    #     bool: True if deletion was successful.
    #
    # Raises:
    #     NotFoundException: If the category does not exist.
    # -------------------------------------------------------------------------
    async def delete_category(self, category_id: str) -> bool:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundException("Category not found")
        
        await self.repo.delete(category_id)
        return True