from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.category import Category
from uuid import UUID
from datetime import datetime
async def create_category(
    session: AsyncSession,
    name: str,
    slug: str
) -> Category:
    
    category = Category(
        name = name,
        slug = slug
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    
    return category

async def get_all_categories(
    session: AsyncSession,
) -> list[Category]:

    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return list(categories)


async def update_admin_categories(
    session: AsyncSession,
    categories_id: UUID,
    name: str,
    slug: str
)-> Category:
    
    categories = await session.get(Category, categories_id)
    if not categories:
        raise ValueError("Categories not found")
    if name is not None:
        categories.name = name
    if slug is not None:
        categories.slug = slug
        
    categories.updated_at = datetime.now()
    await session.commit()
    await session.refresh(categories)
    
    return categories

async def delete_categories(
    session: AsyncSession,
    categories_id: UUID
) -> dict[str, str]:
    category = await session.get(Category, categories_id)
    
    if not category:
        raise ValueError("Category not found")
    
    await session.delete(category)
    await session.commit()
    
    return {"message": "Category deleted successfully"}
