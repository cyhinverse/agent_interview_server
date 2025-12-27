from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    comfirmPassword: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterResponseSchema(BaseModel):
    id: int
    email: EmailStr


class LoginResponseSchema(BaseModel):
    id: int
    email: EmailStr


class ChangePasswordSchema(BaseModel):
    password: str
    confirmPassword: str

class ChangePasswordResponseSchema(BaseModel):
    id: int
    email: EmailStr

