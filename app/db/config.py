from litestar.plugins.sqlalchemy import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from litestar import Litestar
from typing import TYPE_CHECKING
from app.db.models.base import Base
import os
    

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="postgresql+asyncpg://james:james123@db:5432/api_db"
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))
PASSWORD_RESET_BASE_URL= os.getenv("PASSWORD_RESET_BASE_URL")
JWT_ALG = os.getenv("JWT_ALG", "HS256")