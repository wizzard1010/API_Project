from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.articles import Article
from app.db.models.category import Category
from app.db.models.accounts import User
from uuid import UUID


#still need for datetime and uploads#####
async def create_articles(
    session: AsyncSession,
    title: str,
    body: str,
    category_id: UUID,
    author_id: UUID,
    photo_path: str | None = None,
) -> Article:
    category_result = await session.execute(
        select(Category).where(Category.id == category_id)
    )
    category = category_result.scalar_one_or_none()
    
    if category is None:
        raise ValueError("Category does not exist")

    author_result = await session.execute(
        select(User).where(User.id == author_id)
    )
    author = author_result.scalar_one_or_none()

    if author is None:
        raise ValueError("Author does not exist")
    
    article = Article(
        title = title,
        body = body,
        category_id = category_id,
        author_id = author_id,
        photo_path = photo_path,
    )
    
    session.add(article)
    await session.commit()
    await session.refresh(article)
    
    return article
