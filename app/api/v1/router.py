from litestar import Router,get

from app.api.accounts.router import user_router
from app.api.Categories.router import categories_router
from app.api.Articles.router import articles_router

@get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

v1_router = Router(
    path="/api/v1",
    route_handlers=[
        user_router,
        categories_router,    
        articles_router,
    ]
)