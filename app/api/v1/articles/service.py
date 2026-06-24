from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.articles import Article, ArticlesVisibility
from app.db.models.category import Category
from app.db.models.accounts import User
from uuid import UUID

async def create_articles(
    session: AsyncSession,
    title: str,
    body: str,
    category_id: UUID,
    author_id: UUID,
    visibility: ArticlesVisibility= ArticlesVisibility.PUBLIC,
    photo_path: str | None = None,
) -> Article:
    
    article = Article(
        title = title,
        body = body,
        category_id = category_id,
        author_id = author_id,
        visibility = visibility,
        photo_path = photo_path,
    )
    
    session.add(article)
    await session.commit()
    await session.refresh(article)
    
    return article
