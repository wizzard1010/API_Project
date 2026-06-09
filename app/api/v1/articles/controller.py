from litestar import get, post, Router
from litestar.exceptions import HTTPException
from uuid import UUID

from app.db.models.articles import Article
from app.api.v1.articles.service import create_articles
 

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.articles.dto import CreateArticle, ArticleResponse

# @get("/articles")
# async def articles_handler() -> dict[str, str]:
#     return{"modules": "articles"}


#still need for datetime and uploads#####
@post("/articles")
async def create_article(
    data: CreateArticle,
    db_session: AsyncSession
) -> ArticleResponse:
    try: 
        article = await create_articles(
            session = db_session,
            title = data.title,
            body = data.body,
            category_id = data.category_id,
            author_id = data.author_id,
            photo_path = data.photo_path,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article")
    return ArticleResponse(
        id = article.id,
        title = article.title,
        body = article.body,
        category_id= article.category_id,
        author_id = article.author_id,
        photo_path = article.photo_path,
    )
