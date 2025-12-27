from app.features.Auths.Auth_Reponsitory import AuthRepository
from app.features.Auths import Auth_Schema as schema
from app.shared.utils.security import hash_password, verify_password
from app.shared.utils.jwt_utils import create_access_token, create_refresh_token, verify_refresh_token
from app.shared.exceptions import UnauthorizedException, DuplicatedEntityException, ValidationException

class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    async def register(self, data: schema.RegisterSchema):
        if data.password != data.confirmPassword:
            raise ValidationException("Passwords do not match")

        existing_user = await self.repo.get_by_email(data.email)
        if existing_user:
            raise DuplicatedEntityException("Email already exists")

        # Prepare user data
        user_data = {
            "fullName": data.fullName,
            "email": data.email,
            "password": hash_password(data.password)
        }
        
        user = await self.repo.create_user(user_data)
        
        # Generate tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})
        
        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": user
        }

    async def login(self, data: schema.LoginSchema):
        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password):
            raise UnauthorizedException("Incorrect email or password")

        # Generate tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})
        
        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": user
        }

    async def change_password(self, user_id: str, data: schema.ChangePasswordSchema):
        if data.newPassword != data.confirmPassword:
            raise ValidationException("New passwords do not match")

        user = await self.repo.get_by_id(user_id)
        if not user or not verify_password(data.oldPassword, user.password):
            raise UnauthorizedException("Incorrect old password")

        hashed_password = hash_password(data.newPassword)
        return await self.repo.update_password(user_id, hashed_password)

    async def refresh_token(self, refresh_token: str):
 
        payload = verify_refresh_token(refresh_token)
        user_id = payload.get("sub")
  
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found")
            
        access_token = create_access_token(data={"sub": user.id})
        new_refresh_token = create_refresh_token(data={"sub": user.id})
        
        return {
            "accessToken": access_token,
            "refreshToken": new_refresh_token,
            "user": user
        }