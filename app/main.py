from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme, Tag

from app.db.config import sqlalchemy_plugin


from app.api.v1.health_check import health_check

from app.api.v1.accounts.controller import (
    register_user,
    Authenticate_user,
    forget_password,
    Reset_password,
    Get_user_me,
    update_admin,
    Get_admin_user,
    
)

from app.api.v1.categories.controller import Create_category

from app.api.v1.articles.controller import (
    create_article
)

v1_router = Router(
    path="/api/v1",
    route_handlers=[
        register_user,
        Authenticate_user,
        create_article,
        Create_category,
        forget_password,
        Reset_password,
        Get_user_me,
        Get_admin_user,
        update_admin
    ]
)

app =Litestar(
    route_handlers=[v1_router, health_check],
    plugins=[sqlalchemy_plugin],
    openapi_config=OpenAPIConfig(
        title="my api",
        version="1.0.0",
        security=[{"BearerToken":[]}],
        components=Components(
            security_schemes = {
                "BearerToken": SecurityScheme(
                    type = "http",
                    scheme = "bearer",
                )
            }
        )
    )
)
