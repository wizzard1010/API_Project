from litestar import Litestar, get, Router

@get("/users")
async def user_handler() -> dict[str, str]:
    return {"modules": "users"}

user_router = Router(
    path="/accounts",
    route_handlers=[user_handler]
)