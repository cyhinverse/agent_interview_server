from app.features.Users.User_Repository import UserRepository
from app.features.Users.User_Schemas import UserCreate, UserResponse, UserUpdate
from app.shared.exceptions import DuplicatedEntityException, ValidationException, NotFoundException

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    """ Create User """
    async def create_user(self, data: UserCreate) -> UserResponse:
        if len(data.password) < 6:
            raise ValidationException("Password must be at least 6 characters long")
        
        existing = await self.repo.find_by_email(data.email)
        if existing:
            raise DuplicatedEntityException("Email already exists")
            
        new_user = await self.repo.create_user(data)
        return UserResponse(id=new_user.id, email=new_user.email)
    
    """ Find User by ID """
    async def find_user_by_id(self, user_id: str) -> UserResponse:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("Không tìm thấy người dùng này")
        return UserResponse(id=user.id, email=user.email)
    
    """ Delete User by ID """
    async def delete_user_by_id(self, user_id: str) -> UserResponse:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        await self.repo.delete_user_by_id(user_id)
        return UserResponse(id=user.id, email=user.email)
    
    """ Update User by ID """
    async def update_user_by_id(self, user_id: str, data: UserUpdate) -> UserResponse:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
            
        updated_user = await self.repo.update_user_by_id(user_id, data)
        return UserResponse(id=updated_user.id, email=updated_user.email)
