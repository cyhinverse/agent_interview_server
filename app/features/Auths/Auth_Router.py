from fastapi import APIRouter, Depends, Request
from app.features.Auths import Auth_Schema as schema
from app.features.Auths.Auth_Service import AuthService
from app.features.Auths.Auth_Dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auths"])

# -------------------------------------------------------------------------
# Register a new user account.
#
# - **fullName**: The user's full name.
# - **email**: The user's email address (unique).
# - **password**: The user's password (must be confirmed).
# - **confirmPassword**: Must match the password.
#
# Returns an access token and refresh token upon successful registration.
# -------------------------------------------------------------------------
@router.post("/register", response_model=schema.TokenSchema, summary="Register new user")
async def register(data: schema.RegisterSchema, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)

# -------------------------------------------------------------------------
# Authenticate a user and return JWT tokens.
#
# - **email**: The user's email address.
# - **password**: The user's password.
#
# Returns:
#     - **accessToken**: Token for accessing protected routes.
#     - **refreshToken**: Token for renewing access tokens.
#     - **user**: The user profile information.
# -------------------------------------------------------------------------
@router.post("/login", response_model=schema.TokenSchema, summary="Login user")
async def login(data: schema.LoginSchema, service: AuthService = Depends(get_auth_service)):
    return await service.login(data)

# -------------------------------------------------------------------------
# Change the password for the currently authenticated user.
#
# Requires an `Authorization: Bearer <token>` header.
#
# - **oldPassword**: The user's current password.
# - **newPassword**: The new desired password.
# - **confirmPassword**: Must match the new password.
# -------------------------------------------------------------------------
@router.post("/change-password", summary="Change password")
async def change_password(
    data: schema.ChangePasswordSchema, 
    request: Request,
    service: AuthService = Depends(get_auth_service)
):
    user_id = request.state.user.get("sub")
    return await service.change_password(user_id, data)

# -------------------------------------------------------------------------
# Obtain a new access token using a valid refresh token.
#
# This is used when the short-lived access token has expired.
#
# - **refresh_token**: The long-lived refresh token provided during login.
# -------------------------------------------------------------------------
@router.post("/refresh", response_model=schema.TokenSchema, summary="Refresh access token")
async def refresh(refresh_token: str, service: AuthService = Depends(get_auth_service)):
    return await service.refresh_token(refresh_token)