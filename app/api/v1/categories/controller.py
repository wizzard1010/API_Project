from litestar import get, post, Router
from litestar.exceptions import HTTPException

from app.db.models.category import Category
from app.api.v1.categories.service import create_category

from app.api.v1.categories.dto import (
    RegisterCategory,
    CategoryResponse
)

from pydantic import BaseModel
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

# @get("/categories")
# async def categories_handler() -> dict[str, str]:
#     return{"modules": "categories"}

@post("/categories")
async def Create_category(
    data: RegisterCategory,
    db_session: AsyncSession
) -> CategoryResponse:
    try:
        category = await create_category(
            session= db_session,
            name= data.name,
            slug= data.slug
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid category")
    return CategoryResponse(
        id = category.id,
        name = category.name,
        slug = category.slug
    )