from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User

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