from litestar import get, post, Request, patch, delete
from litestar.exceptions import HTTPException
from uuid import UUID
from app.db.models.accounts import User, UserRole
from app.api.v1.articles.service import (
    create_articles,
    get_article_visibility,
    get_article_by_id,
    update_article,
    delete_articles,
    modify_article,
    search_article,)
from app.api.v1.articles.security import get_user_from_header
from app.db.models.articles import ArticlesVisibility, Article
from sqlalchemy.ext.asyncio import AsyncSession
from app.authentication import jwt_auth
from typing import Optional

from app.api.v1.articles.dto import CreateArticle, ArticleResponse, ArticleUpdate

def article_return(article)->ArticleResponse:
    return ArticleResponse(
        id=article.id,
        title=article.title,
        body=article.body,
        category_id=article.category_id,
        author_id=article.author_id,
        photo_path=article.photo_path,
        visibility=article.visibility
    )

@post("/articles", middleware=[jwt_auth.middleware], security=[{"BearerToken": []}])
async def list_articles(
    data: CreateArticle,
    request:Request,
    db_session: AsyncSession
)-> ArticleResponse:
    token_user = request.user
    user = await db_session.get(User, token_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # allow only ADMIN or AUTHOR
    if not (user.role == UserRole.ADMIN or user.role == UserRole.AUTHOR):
        raise HTTPException(status_code=403, detail="Permission denied")
    articles = await create_articles(
        session= db_session,
        title= data.title,
        body = data.body,
        category_id= data.category_id,
        author_id= data.author_id,
        visibility= data.visibility,
        #photo_path= data.photo_path
    )
    return article_return(articles)

@get("/articles")
async def get_articles(
    request: Request,
    db_session: AsyncSession
)-> list[ArticleResponse]:
    is_private = False
    
    user = await get_user_from_header(
        request= request,
        db_session= db_session
    )
    if user and user.is_active:
        is_private = True

    article = await get_article_visibility(
        session= db_session,
        is_private= is_private
    )
    return [article_return(a)
            for a in article]


@get("/articles/{article_id:uuid}")
async def get_article_id(
    db_session:AsyncSession,
    request: Request,
    article_id: UUID,
)-> ArticleResponse:
    
    article = await get_article_by_id(
        session = db_session,
        article_id = article_id
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.visibility == ArticlesVisibility.PUBLIC:
        return article_return(article)
    
    user = await get_user_from_header(
        request= request,
        db_session= db_session
    )
    if not user or not user.is_active:
        raise HTTPException(status_code= 404, detail="User not found")
    
    return article_return(article)

#still need to do author ownership
@patch("/articles/{article_id:uuid}",middleware=[jwt_auth.middleware], security=[{"BearerToken":[]}])
async def update_admin_author_article(
    article_id: UUID,
    data:ArticleUpdate,
    request: Request,
    db_session: AsyncSession
)-> ArticleResponse:
    token_user = request.user
    admin_user = await db_session.get(User, token_user.id)
    
    if not admin_user:
        raise HTTPException(status_code=404, detail="Invalid user")
    
    article = await get_article_by_id(session=db_session, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if not modify_article(user=admin_user, author_id=article.author_id):
        raise HTTPException(status_code=403, detail="Permission Denied")
 
    try: 
        article = await update_article(
            session = db_session,
            article_id= article_id,
            title = data.title,
            body = data.body,
            visibility= data.visibility
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Article not found")
    return article_return(article)
        
#still need author owndership
@delete("/articles/{article_id:uuid}", status_code=200, middleware=[jwt_auth.middleware], security=[{"BearerToken": []}])
async def delete_article(
    article_id: UUID,
    request:Request,
    db_session: AsyncSession
)-> dict[str, str]:
    token_user = request.user
    admin_user = await db_session.get(User, token_user.id)
    if not admin_user:
        raise HTTPException(status_code=404, detail="Invalid user")

    article = await get_article_by_id(session=db_session, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if not modify_article(
        user=admin_user,
        author_id=article.author_id
    ):
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        await delete_articles(
            session=db_session,
            article_id=article_id
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "article deleted successfully"}
    
@get("/articles/search")
async def search_articles(
    request:Request,
    db_session: AsyncSession,
    q : str | None,
    category: UUID | None,
    page : int = 1,
    page_size : int = 10,
)-> list[ArticleResponse]: 
    is_private = False
    
    user = await get_user_from_header(
        request=request,
        db_session=db_session
    )
    if user and user.is_active:
        is_private = True

    article = await search_article(
        session=db_session,
        q = q,
        category= category,
        page= page,
        page_size=page_size
    )
    return [article_return(a)
            for a in article]
    