from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.category import Category

async def create_category(
    session: AsyncSession,
    name: str,
    slug: str
) -> Category:
    result = await session.execute(select(Category).where(Category.name == name))
    
    category = Category(
        name = name,
        slug = slug
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    
    return category

