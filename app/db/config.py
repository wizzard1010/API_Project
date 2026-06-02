from litestar.plugins.sqlalchemy import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from litestar import Litestar
from typing import TYPE_CHECKING
from app.db.models.base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
    
    

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="postgresql+asyncpg://james:james123@db:5432/api_db"
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
