from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import uvicorn

load_dotenv()

from app.shared.database import db
from app.shared.middlewares.auth_middleware import AuthMiddleware
from app.features.Auths.Auth_Router import router as auth_router
from app.features.Users.User_Router import router as users_router
from app.features.InterviewCategories.InterviewCategory_Router import router as interview_categories_router
from app.features.InterviewSessions.InterviewSession_Router import router as interview_sessions_router
from app.features.QuestionBanks.QuestionBank_Router import router as question_banks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(
    title="AI Interview Platform API",
    description="Backend for AI Interview Platform using FastAPI and Prisma",
    version="1.2.0",
    lifespan=lifespan
)

app.add_middleware(AuthMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(interview_categories_router)
app.include_router(interview_sessions_router)
app.include_router(question_banks_router)
@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
