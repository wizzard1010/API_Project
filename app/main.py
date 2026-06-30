from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme

from app.db.config import sqlalchemy_plugin


from app.api.v1.health_check import health_check

#User
from app.api.v1.accounts.controller import (
    register_user,
    Authenticate_user,
    forget_password,
    Reset_password,
    Get_user_me,
    update_admin,
    Get_admin_user,
)

#Category
from app.api.v1.categories.controller import(
    list_category,
    get_categories,
    update_categories,
    delete_category,
)

#Article
from app.api.v1.articles.controller import (
    list_articles,
    get_articles,
    get_article_id,
    update_admin_author_article,
    delete_article,
)

v1_router = Router(
    path="/api/v1",
    route_handlers=[
        register_user,
        Authenticate_user,
        list_articles,
        list_category,
        get_categories,
        update_categories,
        delete_category,
        forget_password,
        Reset_password,
        Get_user_me,
        Get_admin_user,
        update_admin,
        get_articles,
        get_article_id,
        update_admin_author_article,
        delete_article,
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
