from fastapi import APIRouter, Depends, HTTPException
from app.features.users.schemas import UserCreate, UserResponse
from app.features.users.service import UserService
from app.features.users.dependencies import get_user_service
from app.shared.exceptions import DomainException

router = APIRouter(prefix="/users", tags=["Người Dùng (Users)"])

@router.post("/register", response_model=UserResponse, summary="Đăng ký người dùng mới")
async def register(
    data: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    try:
        # Vì dùng Prisma (async), router cũng phải dùng async/await
        return await service.register_user(data)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))
