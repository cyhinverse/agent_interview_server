from typing import List
from uuid import uuid4
from datetime import datetime
from app.features.InterviewSessions.InterviewSession_Repository import InterviewSessionRepository
from app.features.InterviewSessions.InterviewSession_Schema import InterviewSessionCreate, InterviewSessionUpdate, InterviewSessionResponse
from app.features.InterviewCategories.InterviewCategory_Repository import InterviewCategoryRepository
from app.shared.exceptions import NotFoundException
from pipecat.audio.vad.silero import SileroVADAnalyzer



class InterviewSessionService:
    # -------------------------------------------------------------------------
    # Service class responsible for business logic related to Interview Sessions.
    # -------------------------------------------------------------------------

    def __init__(self, repo: InterviewSessionRepository, category_repo: InterviewCategoryRepository):
        self.repo = repo
        self.category_repo = category_repo

    # -------------------------------------------------------------------------
    # Create a new interview session.
    #
    # 1. Verifies if the category exists.
    # 2. Generates a mock Daily.co room URL (integration to be added).
    # 3. Creates the session in the database.
    #
    # Args:
    #     user_id (str): The ID of the authenticated user.
    #     data (InterviewSessionCreate): The session creation data.
    #
    # Returns:
    #     InterviewSessionResponse: The created session details.
    #
    # Raises:
    #     NotFoundException: If the category does not exist.
    # -------------------------------------------------------------------------
    async def create_session(self, user_id: str, data: InterviewSessionCreate) -> InterviewSessionResponse:
        # 1. Verify Category
        category = await self.category_repo.get_by_id(data.categoryId)
        if not category:
            raise NotFoundException("Interview Category not found")

        # 2. Generate Mock Daily Room URL (TODO: Integrate real Daily.co API)
        # Using a placeholder for now to allow development to proceed without API keys.
        room_name = f"interview-{uuid4().hex[:8]}"
        mock_daily_url = f"https://your-domain.daily.co/{room_name}"

        session_data = {
            "userId": user_id,
            "categoryId": data.categoryId,
            "dailyRoomUrl": mock_daily_url,
            "status": "SCHEDULED"
        }

        # 3. Create Session
        session = await self.repo.create(session_data)
        return InterviewSessionResponse.model_validate(session)

    # -------------------------------------------------------------------------
    # Retrieve a specific session by ID.
    #
    # Args:
    #     session_id (str): The UUID of the session.
    #     user_id (str): The ID of the current user (for authorization check).
    #
    # Returns:
    #     InterviewSessionResponse: The session details.
    #
    # Raises:
    #     NotFoundException: If session not found or belongs to another user.
    # -------------------------------------------------------------------------
    async def get_session_by_id(self, session_id: str, user_id: str) -> InterviewSessionResponse:
        session = await self.repo.get_by_id(session_id)
        if not session or session.userId != user_id:
            raise NotFoundException("Interview Session not found")
        
        return InterviewSessionResponse.model_validate(session)

    # -------------------------------------------------------------------------
    # List all sessions for the current user.
    #
    # Args:
    #     user_id (str): The ID of the current user.
    #     skip (int): Pagination skip.
    #     take (int): Pagination take.
    #
    # Returns:
    #     List[InterviewSessionResponse]: List of user's sessions.
    # -------------------------------------------------------------------------
    async def list_user_sessions(self, user_id: str, skip: int = 0, take: int = 20) -> List[InterviewSessionResponse]:
        sessions = await self.repo.get_all_by_user(user_id, skip, take)
        return [InterviewSessionResponse.model_validate(s) for s in sessions]

    # -------------------------------------------------------------------------
    # Update session details (e.g., status, end time).
    #
    # Args:
    #     session_id (str): The UUID of the session.
    #     user_id (str): The ID of the current user.
    #     data (InterviewSessionUpdate): Fields to update.
    #
    # Returns:
    #     InterviewSessionResponse: The updated session details.
    # -------------------------------------------------------------------------
    async def update_session(self, session_id: str, user_id: str, data: InterviewSessionUpdate) -> InterviewSessionResponse:
        # Check existence and ownership
        session = await self.repo.get_by_id(session_id)
        if not session or session.userId != user_id:
            raise NotFoundException("Interview Session not found")

        update_data = data.model_dump(exclude_unset=True)
        
        # If status is changing to COMPLETED, auto-set endTime if not provided
        if update_data.get("status") == "COMPLETED" and not update_data.get("endTime"):
            update_data["endTime"] = datetime.utcnow()

        updated_session = await self.repo.update(session_id, update_data)
        return InterviewSessionResponse.model_validate(updated_session)

    # -------------------------------------------------------------------------
    # Delete a session.
    #
    # Args:
    #     session_id (str): The UUID of the session.
    #     user_id (str): The ID of the current user.
    # -------------------------------------------------------------------------
    async def delete_session(self, session_id: str, user_id: str):
        session = await self.repo.get_by_id(session_id)
        if not session or session.userId != user_id:
            raise NotFoundException("Interview Session not found")
            
        await self.repo.delete(session_id)
    


    