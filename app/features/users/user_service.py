from app.features.Users.User_Repository import UserRepository
from app.features.Users.User_Schemas import UserCreate, UserResponse, UserUpdate
from app.shared.exceptions import DuplicatedEntityException, ValidationException, NotFoundException
from app.shared.utils.security import hash_password

class UserService:
    # -------------------------------------------------------------------------
    # Service class responsible for business logic related to User management.
    # -------------------------------------------------------------------------
    
    def __init__(self, repo: UserRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # Create a new user ensuring email uniqueness and password hashing.
    #
    # Args:
    #     data (UserCreate): The data for creating a new user.
    #
    # Returns:
    #     UserResponse: The created user's details.
    #
    # Raises:
    #     DuplicatedEntityException: If the email already exists.
    # -------------------------------------------------------------------------
    async def create_user(self, data: UserCreate) -> UserResponse:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise DuplicatedEntityException("Email already exists")
            
        user_data = data.model_dump()
        user_data["password"] = hash_password(data.password)
        
        new_user = await self.repo.create(user_data)
        return UserResponse.model_validate(new_user)
    
    # -------------------------------------------------------------------------
    # Retrieve a user by their ID.
    #
    # Args:
    #     user_id (str): The unique ID of the user.
    #
    # Returns:
    #     UserResponse: The found user's details.
    #
    # Raises:
    #     NotFoundException: If the user does not exist.
    # -------------------------------------------------------------------------
    async def get_user_by_id(self, user_id: str) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)
    
    # -------------------------------------------------------------------------
    # Retrieve a paginated list of all users.
    #
    # Args:
    #     skip (int): Number of records to skip.
    #     take (int): Number of records to return.
    #
    # Returns:
    #     List[UserResponse]: A list of user details.
    # -------------------------------------------------------------------------
    async def get_all_users(self, skip: int = 0, take: int = 20):
        users = await self.repo.get_all(skip=skip, take=take)
        return [UserResponse.model_validate(u) for u in users]
    
    # -------------------------------------------------------------------------
    # Update user details by ID. Hashes password if it is being updated.
    #
    # Args:
    #     user_id (str): The ID of the user to update.
    #     data (UserUpdate): The fields to update.
    #
    # Returns:
    #     UserResponse: The updated user's details.
    #
    # Raises:
    #     NotFoundException: If the user does not exist.
    # -------------------------------------------------------------------------
    async def update_user(self, user_id: str, data: UserUpdate) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
            
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
            
        updated_user = await self.repo.update(user_id, update_data)
        return UserResponse.model_validate(updated_user)
    
    # -------------------------------------------------------------------------
    # Delete a user by ID.
    #
    # Args:
    #     user_id (str): The ID of the user to delete.
    #
    # Returns:
    #     bool: True if deletion was successful.
    #
    # Raises:
    #     NotFoundException: If the user does not exist.
    # -------------------------------------------------------------------------
    async def delete_user(self, user_id: str) -> bool:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        await self.repo.delete(user_id)
        return True
