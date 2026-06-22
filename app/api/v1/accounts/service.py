from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.accounts import User, UserRole
from uuid import UUID
from datetime import datetime
from litestar.security.jwt import Token
from litestar.exceptions import HTTPException
from app.db.config import (JWT_ALG, JWT_SECRET, JWT_EXPIRES_MIN, PASSWORD_RESET_BASE_URL)
from app.api.v1.accounts.security import user_access_token


async def create_user(
    session: AsyncSession,
    email: str,
    password_hash: str

) -> User:
    result = await session.execute(select(User).where(User.email == email))
    
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise ValueError("User already exists")
    
    user = User(
        email = email,
        password_hash = password_hash
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return user

async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str
) -> User:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise ValueError("Invalid email or password")
    
    if user.password_hash != password:
        raise ValueError("Invalid email or password")
    
    return user

async def generate_password_reset_with_token(
    session: AsyncSession,
    email:str
)-> str:
    
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise ValueError("User not found")
    
    token = user_access_token(user.id)
    if not PASSWORD_RESET_BASE_URL:
        raise ValueError("PASSWORD_RESET_BASE_URL is not configured")

    # include the token in the reset link
    reset_link = f"{PASSWORD_RESET_BASE_URL}?token={token}"
    return reset_link

async def password_reset(
    session:AsyncSession,
    token: str,
    new_password: str
)-> None:
    decode_token = Token.decode(encoded_token=token, secret=JWT_SECRET, algorithm=JWT_ALG)
        
    user_id = UUID(decode_token.sub)
    user = await session.get(User, user_id)
        
    if not user:
        raise ValueError("User not found")
    user.password_hash = new_password
    user.updated_at = datetime.now()
    await session.commit()

def role(user: User, roles: list[UserRole]) -> None:
    if user.role not in roles:
        raise HTTPException(status_code=403, detail="Invalid User")

async def get_user_by_id(
    session: AsyncSession,
    user_id: UUID    
)-> Optional[User]:
    result = await session.execute(select(User).where(User.id == user_id))
    user =  result.scalar_one_or_none()
    
    return user

async def get_all_user(session: AsyncSession)-> list[User]:
    result = await session.execute(select(User))
    users = list(result.scalars().all())
    
    return users

async def update_admin_user(
    session: AsyncSession,
    user_id: UUID,
    role: UserRole| None=None,
    is_active: bool| None=None,
)-> User:
    
    user = await session.get(User, user_id)
    
    if not user:
        raise ValueError("User not found")
    
    if role is not None:
        user.role = role
    if is_active is not None:
        user.is_active = is_active
    
    user.updated_at = datetime.now()
    await session.commit()
    await session.refresh(user)
    
    return user
