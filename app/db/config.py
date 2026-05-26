from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from litestar import Litestar


db_config = SQLAlchemyAsyncConfig(
    connection_string="postgresql+asyncpg://james:james123@db:5432/api_db"
)
plugin = SQLAlchemyInitPlugin(config=db_config)
