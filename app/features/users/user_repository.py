from prisma.models import User
from app.shared.database import db
from app.features.Users.User_Schemas import UserCreate, UserUpdate

class UserRepository:
    async def create(self, data: dict) -> User:
        return await db.user.create(data=data)

    async def get_by_email(self, email: str) -> User:
        return await db.user.find_unique(where={"email": email})

    async def get_by_id(self, user_id: str) -> User:
        return await db.user.find_unique(where={"id": user_id})

    async def get_all(self, skip: int = 0, take: int = 20):
        return await db.user.find_many(skip=skip, take=take, order={"createdAt": "desc"})

    async def update(self, user_id: str, data: dict) -> User:
        return await db.user.update(where={"id": user_id}, data=data)

    async def delete(self, user_id: str) -> User:
        return await db.user.delete(where={"id": user_id})
