from fastapi import Depends
from app.features.users.repository import UserRepository
from app.features.users.service import UserService

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


