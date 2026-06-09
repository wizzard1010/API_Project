from litestar import get, post, Router
from litestar.exceptions import HTTPException

from app.db.models.user import User
from app.api.v1.accounts.service import create_user, login_user

from app.api.v1.accounts.dto import (
    RegisterRequest,
    LoginRequest
)

from pydantic import BaseModel
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession


    

# testing
  
# @get("/users")
# async def user_handler() -> dict[str, str]:
#     return {"modules": "users"}

@post("/register")
async def register_user(
    data: RegisterRequest,
    db_session: AsyncSession
) -> dict[str, str | bool]:
    try:
        user = await create_user(
            session= db_session,
            email= data.email,
            password_hash= data.password,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return {
        "id": str(user.id),
        "email": user.email,
        "role": user.role.value,
        "is_active": user.is_active,
    }
    

@post("/login")
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