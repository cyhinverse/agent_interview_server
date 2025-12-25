from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate, UserResponse, UserUpdate
from app.shared.exceptions import DuplicatedEntityException, ValidationException, NotFoundException

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    """ Đăng ký User """
    async def register_user(self, data: UserCreate) -> UserResponse:
        if len(data.password) < 6:
            raise ValidationException("Mật khẩu phải từ 6 ký tự trở lên")
        
        existing = await self.repo.find_by_email(data.email)
        if existing:
            raise DuplicatedEntityException("Email này đã được đăng ký rồi")
            
        new_user = await self.repo.create(data)
        return UserResponse(id=new_user.id, email=new_user.email)
    
    """ Tìm User theo ID """
    async def find_user_by_id(self, user_id: str) -> UserResponse:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("Không tìm thấy người dùng này")
        return UserResponse(id=user.id, email=user.email)
    
    """ Xóa User theo ID """
    async def delete_user_by_id(self, user_id: str) -> UserResponse:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("Không tìm thấy người dùng để xóa")
        
        await self.repo.delete_user_by_id(user_id)
        return UserResponse(id=user.id, email=user.email)
    
    """ Cập nhật User theo ID """
    async def update_user_by_id(self, user_id: str, data: UserUpdate) -> UserResponse:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("Không tìm thấy người dùng để cập nhật")
            
        updated_user = await self.repo.update_user_by_id(user_id, data)
        return UserResponse(id=updated_user.id, email=updated_user.email)
