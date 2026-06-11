from litestar import post, get, Request
from litestar.exceptions import HTTPException

from app.db.models.user import User
from app.api.v1.accounts.service import create_user, login_user, generate_password_reset_token, password_reset

from app.api.v1.accounts.dto import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    ForgetPassword,
    ResetPassword
)

from pydantic import BaseModel
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID
    

# testing
  
# @get("/users")
# async def user_handler() -> dict[str, str]:
#     return {"modules": "users"}

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
async def login(
    data: LoginRequest,
    db_session: AsyncSession
) -> dict[str, str]:
    try:
        user = await login_user(
            session = db_session,
            email = data.email,
            password = data.password
        )
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {
        "id": str(user.id),
        "email": user.email,
        "role" : user.role
    }

@post("/auth/password/forget")
async def forget_password(
    data:ForgetPassword,
    db_session: AsyncSession
) -> dict[str, str]:
    try :
        reset_link = await generate_password_reset_token(
        session = db_session,
        email = data.email
    )
    except ValueError:
        raise HTTPException(status_code=400, detail="expired token")
    
    return {
        "reset_link": reset_link
    }

###test test
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

