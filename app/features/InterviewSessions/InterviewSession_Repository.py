from typing import List, Optional
from prisma.models import InterviewSession
from app.shared.database import db

class InterviewSessionRepository:
    # -------------------------------------------------------------------------
    # Repository for handling Interview Session-related database operations.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Create a new interview session.
    #
    # Args:
    #     data (dict): Dictionary containing session data (userId, categoryId, etc.).
    #
    # Returns:
    #     InterviewSession: The created session object.
    # -------------------------------------------------------------------------
    async def create(self, data: dict) -> InterviewSession:
        return await db.interviewsession.create(data=data)

    # -------------------------------------------------------------------------
    # Retrieve a session by its unique ID.
    #
    # Includes related User and Category data.
    #
    # Args:
    #     session_id (str): The unique UUID of the session.
    #
    # Returns:
    #     Optional[InterviewSession]: The session object, or None if not found.
    # -------------------------------------------------------------------------
    async def get_by_id(self, session_id: str) -> Optional[InterviewSession]:
        return await db.interviewsession.find_unique(
            where={"id": session_id},
            include={"user": True, "category": True}
        )

    # -------------------------------------------------------------------------
    # Retrieve all sessions for a specific user.
    #
    # Args:
    #     user_id (str): The UUID of the user.
    #     skip (int): Number of records to skip.
    #     take (int): Number of records to return.
    #
    # Returns:
    #     List[InterviewSession]: A list of session objects.
    # -------------------------------------------------------------------------
    async def get_all_by_user(self, user_id: str, skip: int = 0, take: int = 20) -> List[InterviewSession]:
        return await db.interviewsession.find_many(
            where={"userId": user_id},
            skip=skip,
            take=take,
            order={"createdAt": "desc"},
            include={"category": True}
        )

    # -------------------------------------------------------------------------
    # Update an existing session.
    #
    # Args:
    #     session_id (str): The UUID of the session to update.
    #     data (dict): Dictionary containing fields to update.
    #
    # Returns:
    #     Optional[InterviewSession]: The updated session object.
    # -------------------------------------------------------------------------
    async def update(self, session_id: str, data: dict) -> Optional[InterviewSession]:
        return await db.interviewsession.update(
            where={"id": session_id},
            data=data,
            include={"category": True}
        )

    # -------------------------------------------------------------------------
    # Delete a session by its ID.
    #
    # Args:
    #     session_id (str): The UUID of the session to delete.
    #
    # Returns:
    #     Optional[InterviewSession]: The deleted session object.
    # -------------------------------------------------------------------------
    async def delete(self, session_id: str) -> Optional[InterviewSession]:
        return await db.interviewsession.delete(where={"id": session_id})
