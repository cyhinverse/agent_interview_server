from fastapi import Depends
from app.features.Users.User_Repository import UserRepository
from app.features.Users.User_Service import UserService

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)
