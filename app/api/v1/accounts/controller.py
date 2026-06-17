from litestar import post, get, Request
from litestar.exceptions import HTTPException,NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from app.db.models.accounts import User
from app.api.v1.accounts.service import (
    create_user, 
    authenticate_user,
    user_access_token,
    generate_password_reset_with_token,
    password_reset, 
    get_current_user)

from app.api.v1.accounts.dto import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    ForgetPassword,
    ResetPassword,
    LoginResponse
)

from pydantic import BaseModel
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

@post("/auth/register")
async def register_user(
    data: RegisterRequest,
    db_session: AsyncSession
) -> UserResponse:
    try:
        user = await create_user(
            session= db_session,
            email= data.email,
            password_hash= data.password,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        role= user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    

@post("/auth/login")
async def Authenticate_user(
    data: LoginRequest,
    db_session: AsyncSession
) -> LoginResponse:
    try:
        user = await authenticate_user(
            session=db_session,
            email=data.email,
            password=data.password,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invaid username or password")
    token = await user_access_token(user.id)
    
    return LoginResponse(
        access_token=token
    )

@post("/auth/password/forget")
async def forget_password(
    data:ForgetPassword,
    db_session: AsyncSession
) -> dict[str, str]:
    try :
        reset_link = await generate_password_reset_with_token(
        session = db_session,
        email = data.email
    )
    except ValueError:
        raise HTTPException(status_code=400, detail="expired token")
    
    return {
        "reset_link": reset_link
    }

@post("/auth/password/reset")
async def Reset_password(
    data:ResetPassword,
    db_session: AsyncSession
)-> str:
    try:
        await password_reset(
            session = db_session,
            token = data.token,
            new_password=data.new_password,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invaild token")
    
    return "Password reset successful"

@get("/users/me")
async def Get_user_me(
    request: Request,
    db_session: AsyncSession
)-> UserResponse:
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise NotAuthorizedException()
    if not auth_header.startswith("Bearer "):
        raise NotAuthorizedException()
    
    token = auth_header.replace("Bearer", "")
    try:
        user = await get_current_user(
            session= db_session,
            token = token,
        )
    except:
        raise HTTPException(status_code=400, detail="User not found")
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    
    
    # try:
    #     await get_current_user(
    #         session = db_session,
    #         token = request.token
