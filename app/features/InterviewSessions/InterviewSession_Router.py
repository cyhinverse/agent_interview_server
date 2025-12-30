from fastapi import APIRouter, Depends, Request
from typing import List
from app.features.InterviewSessions.InterviewSession_Schema import InterviewSessionCreate, InterviewSessionUpdate, InterviewSessionResponse
from app.features.InterviewSessions.InterviewSession_Service import InterviewSessionService
from app.features.InterviewSessions.InterviewSession_Dependencies import get_interview_session_service

router = APIRouter(prefix="/interview-sessions", tags=["Interview Sessions"])

# -------------------------------------------------------------------------
# Create a new interview session.
#
# Requires Authentication.
#
# - **categoryId**: The ID of the interview category to practice.
#
# Returns the new session with a generated Daily.co room URL.
# -------------------------------------------------------------------------
@router.post("/", response_model=InterviewSessionResponse, summary="Start new session")
async def create_session(
    data: InterviewSessionCreate,
    request: Request,
    service: InterviewSessionService = Depends(get_interview_session_service)
):
    user_id = request.state.user.get("sub")
    return await service.create_session(user_id, data)

# -------------------------------------------------------------------------
# List all interview sessions for the current user.
# -------------------------------------------------------------------------
@router.get("/", response_model=List[InterviewSessionResponse], summary="List my sessions")
async def list_sessions(
    request: Request,
    skip: int = 0,
    take: int = 20,
    service: InterviewSessionService = Depends(get_interview_session_service)
):
    user_id = request.state.user.get("sub")
    return await service.list_user_sessions(user_id, skip, take)

# -------------------------------------------------------------------------
# Get details of a specific session.
#
# Only returns if the session belongs to the current user.
# -------------------------------------------------------------------------
@router.get("/{session_id}", response_model=InterviewSessionResponse, summary="Get session details")
async def get_session(
    session_id: str,
    request: Request,
    service: InterviewSessionService = Depends(get_interview_session_service)
):
    user_id = request.state.user.get("sub")
    return await service.get_session_by_id(session_id, user_id)

# -------------------------------------------------------------------------
# Update a session (e.g., mark as COMPLETED).
# -------------------------------------------------------------------------
@router.put("/{session_id}", response_model=InterviewSessionResponse, summary="Update session")
async def update_session(
    session_id: str,
    data: InterviewSessionUpdate,
    request: Request,
    service: InterviewSessionService = Depends(get_interview_session_service)
):
    user_id = request.state.user.get("sub")
    return await service.update_session(session_id, user_id, data)

# -------------------------------------------------------------------------
# Delete a session.
# -------------------------------------------------------------------------
@router.delete("/{session_id}", summary="Delete session")
async def delete_session(
    session_id: str,
    request: Request,
    service: InterviewSessionService = Depends(get_interview_session_service)
):
    user_id = request.state.user.get("sub")
    await service.delete_session(session_id, user_id)
    return {"message": "Session deleted successfully"}
