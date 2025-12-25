from prisma.models import User
from app.shared.database import db
from app.features.users.schemas import UserCreate, UserUpdate

class UserRepository:
    async def create(self, data: UserCreate) -> User:
        # Chuyển Pydantic thành dict để Prisma hiểu
        return await db.user.create(data=data.dict())

    async def find_by_email(self, email: str) -> User:
        return await db.user.find_unique(where={"email": email})

    async def find_by_id(self, user_id: str) -> User:
        return await db.user.find_unique(where={"id": user_id})

    async def delete_user_by_id(self, user_id: str) -> User:
        return await db.user.delete(where={"id": user_id})

    async def update_user_by_id(self, user_id: str, data: UserUpdate) -> User:
        # Loại bỏ các trường None để không ghi đè dữ liệu cũ bằng giá trị trống
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        return await db.user.update(where={"id": user_id}, data=update_data)
