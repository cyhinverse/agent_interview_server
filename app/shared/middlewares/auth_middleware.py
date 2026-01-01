from fastapi import Request
from fastapi.responses import JSONResponse
from app.shared.utils.jwt_utils import verify_access_token
from app.shared.exceptions import UnauthorizedException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Allow open access to docs, auth, and root (for redirect)
        if (path == "/" or 
            path.startswith("/docs") or 
            path.startswith("/openapi.json") or 
            path.startswith("/auth") or
            path.startswith("/favicon.ico")):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        try:
            token = auth_header.split(" ")[1]
            user_data = verify_access_token(token)
            request.state.user = user_data
        except Exception:
            return JSONResponse(
                status_code=401,
                content={"detail": "Could not validate credentials"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        response = await call_next(request)
        return response
