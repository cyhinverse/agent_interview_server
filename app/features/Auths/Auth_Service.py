
from app.features.Auths.Auth_Reponsitory import AuthRepository
from app.features.Auths import Auth_Schema as schema
from app.shared.utils.security import hash_password, verify_password
from fastapi import HTTPException
class AuthService:
    def __init__(self,repo: AuthRepository):
        self.repo = repo

    def register(self,data: schema.RegisterSchema) -> schema.RegisterResponseSchema:
        hashed_password = hash_password(data.password)
        if not data.password:
            raise HTTPException(status_code=400,detail="Password is required")
        
        if data.password != data.password_confirmation:
            raise HTTPException(status_code=400,detail="Passwords do not match")

        if self.repo.get_user_by_email(data.email):
            raise HTTPException(status_code=400,detail="Email already exists")
        user_data = data.model_dump()
        user_data["password"] = hashed_password
        return self.repo.register(user_data)
    
    def login(self,data: schema.LoginSchema) -> schema.LoginResponseSchema:
        user = self.repo.get_user_by_email(data.email)
        if not user:
            raise HTTPException(status_code=401,detail="Incorrect email or password")
        if not verify_password(data.password,user.password):
            raise HTTPException(status_code=401,detail="Incorrect email or password")
        return self.repo.login(data.model_dump())
    
    def change_password(self,data: schema.ChangePasswordSchema) -> schema.ChangePasswordResponseSchema:
        user = self.repo.get_user_by_email(data.email)
        if not user:
            raise HTTPException(status_code=401,detail="User not found")
        if not verify_password(data.password,user.password):
            raise HTTPException(status_code=401,detail="Incorrect password")
        return self.repo.change_password(data.model_dump())