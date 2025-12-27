from fastapi import APIRouter, Depends, HTTPException, Request
from app.features.Users.User_Schemas import UserCreate, UserResponse
from app.features.Users.User_Service import UserService
from app.features.Users.User_Dependencies import get_user_service
from app.shared.exceptions import DomainException

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=UserResponse, summary="Create new user")
async def register(
    data: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    try:    
        return await service.create_user(data)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse, summary="Get current logged in user")
async def get_me(request: Request):
    current_user = request.state.user
    return current_user

