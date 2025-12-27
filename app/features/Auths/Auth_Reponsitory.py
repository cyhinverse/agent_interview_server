from prisma.models import User
from app.shared.database import db

class AuthRepository:
    async def create_user(self, data: dict) -> User:
        return await db.user.create(data=data)

    async def get_by_email(self, email: str) -> User:
        return await db.user.find_unique(where={"email": email})

    async def get_by_id(self, user_id: str) -> User:
        return await db.user.find_unique(where={"id": user_id})

    async def update_password(self, user_id: str, hashed_password: str) -> User:
        return await db.user.update(
            where={"id": user_id},
            data={"password": hashed_password}
        )