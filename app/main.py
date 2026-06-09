from litestar import Litestar, Router

from app.db.config import sqlalchemy_plugin


from app.api.v1.health_check import health_check

from app.api.v1.accounts.controller import (
    register_user,
    login
)

from app.api.v1.categories.controller import Create_category

from app.api.v1.articles.controller import (
    create_article
)

v1_router = Router(
    path="/api/v1",
    route_handlers=[
        register_user,
        login,
        create_article,
        Create_category, 
    ]
)

app =Litestar(
    route_handlers=[v1_router, health_check],
    plugins=[sqlalchemy_plugin]
)
