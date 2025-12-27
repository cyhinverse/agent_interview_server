from fastapi import APIRouter, Depends, HTTPException
from app.features.users.user_schemas import UserCreate, UserResponse
from app.features.users.user_service import UserService
from app.features.users.dependencies import get_user_service
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
    

