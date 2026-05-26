from litestar import Litestar
from app.api.v1.router import v1_router
from app.db.config import plugin

app = Litestar(
    route_handlers=[v1_router],
    plugins=[plugin]
)