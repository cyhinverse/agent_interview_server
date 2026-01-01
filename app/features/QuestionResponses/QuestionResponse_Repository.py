from typing import List, Optional
from prisma.models import QuestionResponse
from app.shared.database import db

class QuestionResponseRepository:
    # -------------------------------------------------------------------------
    # Repository for handling Question Response related database operations.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Create a new question response.
    #
    # Args:
    #     data (dict): Dictionary containing response data.
    #
    # Returns:
    #     QuestionResponse: The created response object.
    # -------------------------------------------------------------------------
    async def create(self, data: dict) -> QuestionResponse:
        return await db.questionresponse.create(data=data)

    # -------------------------------------------------------------------------
    # Retrieve a question response by its unique ID.
    #
    # Args:
    #     response_id (str): The unique UUID of the response.
    #
    # Returns:
    #     Optional[QuestionResponse]: The response object, or None if not found.
    # -------------------------------------------------------------------------
    async def get_by_id(self, response_id: str) -> Optional[QuestionResponse]:
        return await db.questionresponse.find_unique(
            where={"id": response_id},
            include={"question": True}
        )

    # -------------------------------------------------------------------------
    # Retrieve responses by session ID.
    #
    # Args:
    #     session_id (str): The session UUID.
    #     skip (int): Number of records to skip.
    #     take (int): Number of records to return.
    #
    # Returns:
    #     List[QuestionResponse]: A list of response objects.
    # -------------------------------------------------------------------------
    async def get_by_session(self, session_id: str, skip: int = 0, take: int = 20) -> List[QuestionResponse]:
        return await db.questionresponse.find_many(
            where={"sessionId": session_id},
            skip=skip,
            take=take,
            include={"question": True}
        )

    # -------------------------------------------------------------------------
    # Update an existing response.
    #
    # Args:
    #     response_id (str): The UUID of the response to update.
    #     data (dict): Dictionary containing fields to update.
    #
    # Returns:
    #     Optional[QuestionResponse]: The updated response object.
    # -------------------------------------------------------------------------
    async def update(self, response_id: str, data: dict) -> Optional[QuestionResponse]:
        return await db.questionresponse.update(
            where={"id": response_id},
            data=data,
            include={"question": True}
        )

    # -------------------------------------------------------------------------
    # Delete a response by its ID.
    #
    # Args:
    #     response_id (str): The UUID of the response to delete.
    #
    # Returns:
    #     Optional[QuestionResponse]: The deleted response object.
    # -------------------------------------------------------------------------
    async def delete(self, response_id: str) -> Optional[QuestionResponse]:
        return await db.questionresponse.delete(where={"id": response_id})
