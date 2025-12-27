from app.features.Users.User_Repository import UserRepository
from app.features.Users.User_Schemas import UserCreate, UserResponse, UserUpdate
from app.shared.exceptions import DuplicatedEntityException, ValidationException, NotFoundException
from app.shared.utils.security import hash_password

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate) -> UserResponse:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise DuplicatedEntityException("Email already exists")
            
        user_data = data.model_dump()
        user_data["password"] = hash_password(data.password)
        
        new_user = await self.repo.create(user_data)
        return UserResponse.model_validate(new_user)
    
    async def get_user_by_id(self, user_id: str) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)
    
    async def get_all_users(self, skip: int = 0, take: int = 20):
        users = await self.repo.get_all(skip=skip, take=take)
        return [UserResponse.model_validate(u) for u in users]
    
    async def update_user(self, user_id: str, data: UserUpdate) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
            
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
            
        updated_user = await self.repo.update(user_id, update_data)
        return UserResponse.model_validate(updated_user)
    
    async def delete_user(self, user_id: str) -> bool:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        await self.repo.delete(user_id)
        return True
