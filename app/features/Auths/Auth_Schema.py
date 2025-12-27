from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterSchema(BaseModel):
    fullName: str
    email: EmailStr
    password: str
    confirmPassword: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: str
    fullName: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    accessToken: str
    refreshToken: str
    user: UserResponseSchema

class ChangePasswordSchema(BaseModel):
    oldPassword: str
    newPassword: str
    confirmPassword: str
