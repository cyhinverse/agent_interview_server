from typing import List, Optional
from prisma.models import QuestionBank
from app.shared.database import db

class QuestionBankRepository:
    # -------------------------------------------------------------------------
    # Repository for handling Question Bank related database operations.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Create a new question.
    #
    # Args:
    #     data (dict): Dictionary containing question data.
    #
    # Returns:
    #     QuestionBank: The created question object.
    # -------------------------------------------------------------------------
    async def create(self, data: dict) -> QuestionBank:
        return await db.questionbank.create(data=data)

    # -------------------------------------------------------------------------
    # Retrieve a question by its unique ID.
    #
    # Args:
    #     question_id (str): The unique UUID of the question.
    #
    # Returns:
    #     Optional[QuestionBank]: The question object, or None if not found.
    # -------------------------------------------------------------------------
    async def get_by_id(self, question_id: str) -> Optional[QuestionBank]:
        return await db.questionbank.find_unique(
            where={"id": question_id}
        )

    # -------------------------------------------------------------------------
    # Retrieve all questions.
    #
    # Args:
    #     skip (int): Number of records to skip.
    #     take (int): Number of records to return.
    #
    # Returns:
    #     List[QuestionBank]: A list of question objects.
    # -------------------------------------------------------------------------
    async def get_all(self, skip: int = 0, take: int = 20) -> List[QuestionBank]:
        return await db.questionbank.find_many(
            skip=skip,
            take=take
        )

    # -------------------------------------------------------------------------
    # Retrieve questions by category ID.
    #
    # Args:
    #     category_id (str): The category UUID.
    #     skip (int): Number of records to skip.
    #     take (int): Number of records to return.
    #
    # Returns:
    #     List[QuestionBank]: A list of question objects.
    # -------------------------------------------------------------------------
    async def get_by_category(self, category_id: str, skip: int = 0, take: int = 20) -> List[QuestionBank]:
        return await db.questionbank.find_many(
            where={"categoryId": category_id},
            skip=skip,
            take=take
        )

    # -------------------------------------------------------------------------
    # Update an existing question.
    #
    # Args:
    #     question_id (str): The UUID of the question to update.
    #     data (dict): Dictionary containing fields to update.
    #
    # Returns:
    #     Optional[QuestionBank]: The updated question object.
    # -------------------------------------------------------------------------
    async def update(self, question_id: str, data: dict) -> Optional[QuestionBank]:
        return await db.questionbank.update(
            where={"id": question_id},
            data=data
        )

    # -------------------------------------------------------------------------
    # Delete a question by its ID.
    #
    # Args:
    #     question_id (str): The UUID of the question to delete.
    #
    # Returns:
    #     Optional[QuestionBank]: The deleted question object.
    # -------------------------------------------------------------------------
    async def delete(self, question_id: str) -> Optional[QuestionBank]:
        return await db.questionbank.delete(where={"id": question_id})
