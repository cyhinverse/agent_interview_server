from fastapi import APIRouter, Depends, Request
from typing import List
from app.features.Users.User_Schemas import UserCreate, UserResponse, UserUpdate
from app.features.Users.User_Service import UserService
from app.features.Users.User_Dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

# -------------------------------------------------------------------------
# Create a new user in the system.
#
# - **fullName**: User's full name.
# - **email**: User's email address (must be unique).
# - **password**: User's password (will be hashed).
# -------------------------------------------------------------------------
@router.post("/", response_model=UserResponse, summary="Create new user")
async def create_user(
    data: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(data)

# -------------------------------------------------------------------------
# Get the profile of the currently authenticated user.
#
# This endpoint uses the JWT token from the header to identify the user.
# -------------------------------------------------------------------------
@router.get("/me", response_model=UserResponse, summary="Get current logged in user")
async def get_me(
    request: Request,
    service: UserService = Depends(get_user_service)
):
    # Retrieve user_id from token decoded by AuthMiddleware
    user_id = request.state.user.get("sub")
    return await service.get_user_by_id(user_id)

# -------------------------------------------------------------------------
# Retrieve user details by their unique ID.
#
# - **user_id**: The UUID of the user.
# -------------------------------------------------------------------------
@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_id(user_id)

# -------------------------------------------------------------------------
# Retrieve a list of users with pagination support.
#
# - **skip**: Number of records to skip (default: 0).
# - **take**: Number of records to return (default: 20).
# -------------------------------------------------------------------------
@router.get("/", response_model=List[UserResponse], summary="List all users")
async def list_users(
    skip: int = 0,
    take: int = 20,
    service: UserService = Depends(get_user_service)
):
    return await service.get_all_users(skip, take)

# -------------------------------------------------------------------------
# Update an existing user's information.
#
# Only provided fields will be updated. Passing a password will re-hash it.
# -------------------------------------------------------------------------
@router.put("/{user_id}", response_model=UserResponse, summary="Update user")
async def update_user(
    user_id: str,
    data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return await service.update_user(user_id, data)

# -------------------------------------------------------------------------
# Permanently delete a user from the system.
#
# - **user_id**: The UUID of the user to delete.
# -------------------------------------------------------------------------
@router.delete("/{user_id}", summary="Delete user")
async def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    await service.delete_user(user_id)
    return {"message": "User deleted successfully"}
