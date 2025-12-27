from fastapi import APIRouter, Depends, Request
from app.features.Auths import Auth_Schema as schema
from app.features.Auths.Auth_Service import AuthService
from app.features.Auths.Auth_Dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auths"])

@router.post("/register", response_model=schema.TokenSchema, summary="Register new user")
async def register(data: schema.RegisterSchema, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)

@router.post("/login", response_model=schema.TokenSchema, summary="Login user")
async def login(data: schema.LoginSchema, service: AuthService = Depends(get_auth_service)):
    return await service.login(data)

@router.post("/change-password", summary="Change password")
async def change_password(
    data: schema.ChangePasswordSchema, 
    request: Request,
    service: AuthService = Depends(get_auth_service)
):
    user_id = request.state.user.get("sub")
    return await service.change_password(user_id, data)

@router.post("/refresh", response_model=schema.TokenSchema, summary="Refresh access token")
async def refresh(refresh_token: str, service: AuthService = Depends(get_auth_service)):
    return await service.refresh_token(refresh_token)