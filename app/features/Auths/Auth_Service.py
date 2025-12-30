from app.features.Auths.Auth_Repository import AuthRepository
from app.features.Auths import Auth_Schema as schema
from app.shared.utils.security import hash_password, verify_password
from app.shared.utils.jwt_utils import create_access_token, create_refresh_token, verify_refresh_token
from app.shared.exceptions import UnauthorizedException, DuplicatedEntityException, ValidationException

class AuthService:
    # -------------------------------------------------------------------------
    # Service class for handling authentication logic including registration, login,
    # password management, and token generation.
    # -------------------------------------------------------------------------
    
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    # -------------------------------------------------------------------------
    # Register a new user.
    #
    # 1. Validates that passwords match.
    # 2. Checks if the email already exists in the database.
    # 3. Hashes the password.
    # 4. Creates the user record.
    # 5. Generates JWT access and refresh tokens.
    #
    # Args:
    #     data (schema.RegisterSchema): The registration data provided by the user.
    #
    # Returns:
    #     dict: Contains 'accessToken', 'refreshToken', and the created 'user' object.
    #
    # Raises:
    #     ValidationException: If passwords do not match.
    #     DuplicatedEntityException: If the email already exists.
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Authenticate a user and generate tokens.
    #
    # 1. Retrieves user by email.
    # 2. Verifies the password.
    # 3. Generates new JWT access and refresh tokens.
    #
    # Args:
    #     data (schema.LoginSchema): The login credentials (email and password).
    #
    # Returns:
    #     dict: Contains 'accessToken', 'refreshToken', and the 'user' object.
    #
    # Raises:
    #     UnauthorizedException: If email is not found or password is incorrect.
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Change the password for an authenticated user.
    #
    # 1. Validates that the new passwords match.
    # 2. Verifies the old password.
    # 3. Updates the user's password with a new hash.
    #
    # Args:
    #     user_id (str): The ID of the currently authenticated user.
    #     data (schema.ChangePasswordSchema): The password change request data.
    #
    # Returns:
    #     User: The updated user object.
    #
    # Raises:
    #     ValidationException: If new passwords do not match.
    #     UnauthorizedException: If the old password is incorrect.
    # -------------------------------------------------------------------------
    async def change_password(self, user_id: str, data: schema.ChangePasswordSchema):
        if data.newPassword != data.confirmPassword:
            raise ValidationException("New passwords do not match")

        user = await self.repo.get_by_id(user_id)
        if not user or not verify_password(data.oldPassword, user.password):
            raise UnauthorizedException("Incorrect old password")

        hashed_password = hash_password(data.newPassword)
        return await self.repo.update_password(user_id, hashed_password)

    # -------------------------------------------------------------------------
    # Refresh access token using a valid refresh token.
    #
    # 1. Verifies the signature and expiration of the refresh token.
    # 2. Extracts the user ID ('sub').
    # 3. Checks if the user still exists.
    # 4. Generates a fresh pair of access and refresh tokens.
    #
    # Args:
    #     refresh_token (str): The refresh token string.
    #
    # Returns:
    #     dict: Contains 'accessToken', 'refreshToken', and the 'user' object.
    #
    # Raises:
    #     UnauthorizedException: If the token is invalid, expired, or the user is not found.
    # -------------------------------------------------------------------------
    async def refresh_token(self, refresh_token: str):
        # 1. Verify refresh token
        payload = verify_refresh_token(refresh_token)
        user_id = payload.get("sub")
        
        # 2. Check if user still exists
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found")
            
        # 3. Generate new token pair
        access_token = create_access_token(data={"sub": user.id})
        new_refresh_token = create_refresh_token(data={"sub": user.id})
        
        return {
            "accessToken": access_token,
            "refreshToken": new_refresh_token,
            "user": user
        }