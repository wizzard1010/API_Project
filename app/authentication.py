from litestar.security.jwt import JWTAuth, Token
from app.db.models.accounts import User
from uuid import UUID
from app.db.config import JWT_SECRET
from litestar.connection import ASGIConnection


async def retrieve_user_handler(token: Token, connection:ASGIConnection)-> User:
    return User(id=UUID(token.sub))


jwt_auth = JWTAuth[User](
    token_secret=JWT_SECRET,
    retrieve_user_handler= retrieve_user_handler,
)