from litestar import Litestar, get, Router

@get("/categories")
async def categories_handler() -> dict[str, str]:
    return{"modules": "categories"}

categories_router = Router(
    path="/cat",
    route_handlers=[categories_handler],
)