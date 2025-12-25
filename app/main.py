from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.shared.database import db

# Import các Router từ các tính năng (features)
from app.features.users.router import router as users_router
from app.features.interviews.router import router as interviews_router

# 1. Quản lý vòng đời kết nối Database (Prisma)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khi khởi động Server: Kết nối Database
    await db.connect()
    yield
    # Khi tắt Server: Ngắt kết nối Database
    await db.disconnect()

# 2. Khởi tạo ứng dụng FastAPI chính với lifespan
app = FastAPI(
    title="Simple AI Backend (Prisma)",
    description="Backend sử dụng Prisma và PostgreSQL",
    version="1.1.0",
    lifespan=lifespan
)

# 3. Đăng ký các Router vào app chính
# Mỗi router sẽ quản lý một nhóm URL riêng biệt
app.include_router(users_router)
app.include_router(interviews_router)

# 4. Trang mặc định - Tự động chuyển hướng về trang tài liệu (Swagger UI)
@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")

# 5. Chạy server trực tiếp bằng lệnh: python -m app.main
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
