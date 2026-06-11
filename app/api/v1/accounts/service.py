from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from uuid import UUID
from datetime import timedelta
from litestar.security.jwt import JWTAuth, Token
from litestar.connection import ASGIConnection

import os

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

async def login_user(
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


JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))
PASSWORD_RESET_BASE_URL= os.getenv("PASSWORD_RESET_BASE_URL")
JWT_ALG = os.getenv("JWT_ALG", "HS256")


async def retrieve_user_handler(token: Token, connection:ASGIConnection)-> User:
    return User(id=UUID(token.sub))


jwt_auth = JWTAuth[User](
    token_secret=JWT_SECRET,
    retrieve_user_handler= retrieve_user_handler,
)

async def create_password_token(user_id:UUID)-> str:
    token = jwt_auth.create_token(
        identifier=str(user_id),
        token_expiration=timedelta(minutes=JWT_EXPIRES_MIN),
    )
    return token

async def generate_password_reset_token(
    session: AsyncSession,
    email:str
)-> str:
    
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise ValueError("User not found")
    
    token = await create_password_token(user.id)
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
    
    await session.commit()