from litestar import get, post, Request, patch, delete
from litestar.exceptions import HTTPException
from typing import Optional
from app.api.v1.categories.service import (
    create_category,
    get_all_categories,
    update_admin_categories,
    delete_categories,
)

from app.api.v1.categories.dto import (
    RegisterCategory,
    CategoryResponse,
    CategoriesUpdate
)
from app.db.models.accounts import User, UserRole
from app.db.models.category import Category
from app.authentication import jwt_auth
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

def categories_return(category) -> CategoryResponse:
    return CategoryResponse(
        id = category.id,
        name = category.name,
        slug = category.slug
    )
    
#POST   /api/v1/categories (admin)
@post("/categories", middleware=[jwt_auth.middleware], security=[{"BearerToken":[]}])
async def list_category(
    data: RegisterCategory,
    request: Request,
    db_session: AsyncSession
) -> CategoryResponse:
    token_user = request.user
    user = await db_session.get(User, token_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role!= UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")
    category = await create_category(
        session= db_session,
        name = data.name,
        slug = data.slug
    )
    return categories_return(category)

@get("/categories")
async def get_categories(
    db_session:AsyncSession
)-> list[CategoryResponse]:
    categories = await get_all_categories(session=db_session)
    
    return [categories_return(
        c
        ) for c in categories]

@patch("/categories/{categories_id:uuid}", middleware=[jwt_auth.middleware], security=[{"BearerToken":[]}])
async def update_categories(
    categories_id: UUID,
    data: CategoriesUpdate,
    request: Request,
    db_session: AsyncSession
)-> CategoryResponse:
    token_user = request.user
    admin_user = await db_session.get(User, token_user.id)
    if not admin_user:
        raise HTTPException(status_code=404, detail="Invalid user")
    if admin_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")
    try:
        categories = await update_admin_categories(
            session= db_session,
            categories_id= categories_id,
            name = data.name,
            slug = data.slug
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories_return(categories)

@delete("/categories/{categories_id:uuid}", status_code=200, middleware=[jwt_auth.middleware], security=[{"BearerToken":[]}])
async def delete_category(
    categories_id: UUID,
    request: Request,
    db_session: AsyncSession
)-> Optional[None]:
    token_user = request.user
    admin_user = await db_session.get(User, token_user.id)
    if not admin_user:
        raise HTTPException(status_code=404, detail="Invalid user")
    if admin_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Permission Denied")
    try:
        categories = await delete_categories(
            session= db_session,
            categories_id= categories_id
        )
    except ValueError:
       raise HTTPException(status_code=404, detail="Category not found")
    return None
    