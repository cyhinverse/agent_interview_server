from fastapi import APIRouter,Depends, HTTPException
from app.features.Auths.Auth_Schema import RegisterSchema,LoginSchema,RegisterResponseSchema,LoginResponseSchema,ChangePasswordSchema
from app.features.Auths.Auth_Service import AuthService
from app.features.Auths.Auth_Dependencies import get_auth_service
from app.shared.exceptions import DomainException


router = APIRouter(prefix="/auth",tags=["Auths"])
@router.post("/register", response_model=RegisterResponseSchema, summary="Register new user")
async def register(data: RegisterSchema, service: AuthService = Depends(get_auth_service)):
    try:
        return await service.register(data)
    except DomainException as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.post("/login", response_model=LoginResponseSchema, summary="Login user")
async def login(data: LoginSchema, service: AuthService = Depends(get_auth_service)):
    try:
        return await service.login(data)
    except DomainException as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.post("/change-password", summary="Change password")
async def change_password(data: ChangePasswordSchema,service: AuthService = Depends(get_auth_service)):
    try:
        return await service.change_password(data)
    except DomainException as e:
        raise HTTPException(status_code=400,detail=str(e))