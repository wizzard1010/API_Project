from litestar import get, post, Router

from app.db.models.user import User
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
@get("/users")
async def user_handler() -> dict[str, str]:
    return {"modules": "users"}


@post("/register")
async def register_account(
    data: RegisterRequest,
    db_session: AsyncSession,
) -> dict:
    result = await db_session.execute(
        select(User).where(User.email==data.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        return {"error": "Email already registered"}
    
    user = User(
        email = data.email,
        password_hash = data.password
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return {
        "id": str(user.id),
        "email" : user.email
    }

user_router = Router(
    path= "/auth",
    route_handlers=[register_account]
)