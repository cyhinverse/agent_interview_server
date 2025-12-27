
from app.features.Auths.Auth_Reponsitory import AuthRepository
from app.features.Auths.Auth_Schema import RegisterSchema,LoginSchema

class AuthService:
    def __init__(self,repo: AuthRepository):
        self.repo = repo

    def register(self,data: RegisterSchema):
        return self.repo.register(data.dict())
    
    def login(self,data: LoginSchema):
        return self.repo.login(data.dict())