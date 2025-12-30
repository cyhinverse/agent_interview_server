from fastapi import Depends
from app.features.Auths.Auth_Repository import AuthRepository
from app.features.Auths.Auth_Service import AuthService


def get_auth_repository() -> AuthRepository:
    return AuthRepository()

def get_auth_service(repo: AuthRepository = Depends(get_auth_repository)) -> AuthService:
    return AuthService(repo)