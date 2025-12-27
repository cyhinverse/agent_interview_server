from fastapi import APIRouter

# Router tạm thời cho tính năng Phỏng Vấn (Interviews)
router = APIRouter(prefix="/interviews", tags=["Phỏng Vấn (Interviews)"])

@router.get("/", summary="Danh sách phỏng vấn")
def list_interviews():
    return {"message": "Đây là danh sách các cuộc phỏng vấn (sẽ được cập nhật sau)"}
    