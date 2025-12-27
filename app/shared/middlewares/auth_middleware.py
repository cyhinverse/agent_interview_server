from fastapi import Request
from app.shared.utils.jwt_utils import verify_access_token
from app.shared.exceptions import UnauthorizedException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/docs") or path.startswith("/openapi.json") or path.startswith("/auth"):
            return await call_next(request)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnauthorizedException("Missing or invalid Authorization header")

        token = auth_header.split(" ")[1]
        
        user_data = verify_access_token(token)
        request.state.user = user_data
        
        response = await call_next(request)
        return response
