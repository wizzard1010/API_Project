from litestar import Litestar, get, Router

@get("/articles")
async def articles_handler() -> dict[str, str]:
    return{"modules": "articles"}

articles_router = Router(
    path="/art",
    route_handlers=[articles_handler],
)