from litestar import Litestar, Router

from app.db.config import sqlalchemy_plugin


from app.api.v1.health_check import health_check
from app.api.v1.accounts.router import user_router
from app.api.v1.categories.router import categories_router
from app.api.v1.articles.router import articles_router

v1_router = Router(
    path="/api/v1",
    route_handlers=[
        user_router,
        categories_router,    
        articles_router,
    ]
)

app = Litestar(
    route_handlers=[v1_router, health_check],
    plugins=[sqlalchemy_plugin]
)