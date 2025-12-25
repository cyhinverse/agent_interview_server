from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. Dữ liệu khi đăng ký
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 2. Dữ liệu khi cập nhật (Các trường đều là Optional - có thể có hoặc không)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# 3. Dữ liệu trả về
class UserResponse(BaseModel):
    id: str
    email: str

    class Config:
        from_attributes = True
