
from app.features.Auths.Auth_Schema import RegisterSchema,LoginSchema
from prisma.models import User
from app.shared.database import db
class AuthRepository:
    async def register(self, data: RegisterSchema) -> User:
        return await db.user.create(data=data.dict())

    async def login(self,data: LoginSchema) -> User: 
        return await db.user.find_unique(where={"email": data.email})