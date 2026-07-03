from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.articles import Article, ArticlesVisibility
from litestar.exceptions import HTTPException
from uuid import UUID
from datetime import datetime
from app.db.models.accounts import User,UserRole

def visibility(article: Article, visibility: list[ArticlesVisibility])-> None:
    if article.visibility not in visibility:
        raise HTTPException(status_code=403, detail="Invalid article")

def modify_article(
    user: User,
    author_id: UUID
)-> bool:
    if user.role == "ADMIN":
        return True
    if user.role == "AUTHOR":
        user.id = author_id
    return True
    


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

async def get_article_visibility(
    session: AsyncSession,
    is_private: bool = False
)-> list[Article]:
    query = select(Article)
    if not is_private:
        query = query.where(Article.visibility == ArticlesVisibility.PUBLIC)
      
    result = await session.execute(query)
    
    return list (result.scalars().all())

async def get_article_by_id(
    session: AsyncSession,
    article_id: UUID,
) -> Article | None:
    result = await session.execute(select(Article).where(Article.id == article_id))
    return result.scalar_one_or_none()

async def update_article(
    session: AsyncSession,
    article_id:UUID,
    title: str,
    body: str,
    visibility: ArticlesVisibility
)-> Article:
    
    article = await session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if title:
       article.title = title 
    if body:
        article.body = body
    if visibility:
        article.visibility = visibility
    article.updated_at = datetime.now()
    await session.commit()
    await session.refresh(article)
    
    return article

async def delete_articles(
    session: AsyncSession,
    article_id: UUID
)-> dict[str, str]:
    article = await session.get(Article, article_id)
    
    if not article:
        raise ValueError("Article not found")
    await session.delete(article)
    await session.commit()
    
    return {"message": "article deleted successully"}

async def search_article(
    session: AsyncSession,
    q: str | None,
    #category: UUID | None,
    page : int | None,
    page_size: int | None,
    is_private:bool = False
)-> list[Article]:
    
    query = select(Article)
    if not is_private:
        query = query.where(Article.visibility == ArticlesVisibility.PUBLIC)
    # if not category is not None:
    #     query = query.where(Article.category_id == category)
    
    if q:
        search_text = f"%{q}%"
        query = query.where(
            (Article.title.contains(search_text)) |
            (Article.body.contains(search_text))
        )
    query = query.limit(page).offset(page_size)
    
    result = await session.execute(query)
    return list(result.scalars().all())