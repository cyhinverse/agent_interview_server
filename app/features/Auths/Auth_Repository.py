from prisma.models import User
from app.shared.database import db

class AuthRepository:
    # -------------------------------------------------------------------------
    # Repository for handling Authentication-related database operations.
    # -------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------
    # Create a new user in the database.
    #
    # Args:
    #     data (dict): Dictionary containing user data (email, password, etc.).
    #
    # Returns:
    #     User: The created User object.
    # -------------------------------------------------------------------------
    async def create_user(self, data: dict) -> User:
        return await db.user.create(data=data)

    # -------------------------------------------------------------------------
    # Retrieve a user by their email address.
    #
    # Args:
    #     email (str): The email address of the user.
    #
    # Returns:
    #     User: The User object if found, otherwise None.
    # -------------------------------------------------------------------------
    async def get_by_email(self, email: str) -> User:
        return await db.user.find_unique(where={"email": email})

    # -------------------------------------------------------------------------
    # Retrieve a user by their unique ID.
    #
    # Args:
    #     user_id (str): The unique identifier of the user.
    #
    # Returns:
    #     User: The User object if found, otherwise None.
    # -------------------------------------------------------------------------
    async def get_by_id(self, user_id: str) -> User:
        return await db.user.find_unique(where={"id": user_id})

    # -------------------------------------------------------------------------
    # Update the password for a specific user.
    #
    # Args:
    #     user_id (str): The unique identifier of the user.
    #     hashed_password (str): The new hashed password to be stored.
    #
    # Returns:
    #     User: The updated User object.
    # -------------------------------------------------------------------------
    async def update_password(self, user_id: str, hashed_password: str) -> User:
        return await db.user.update(
            where={"id": user_id},
            data={"password": hashed_password}
        )