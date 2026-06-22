from litestar.security.jwt import JWTAuth, Token
from litestar.connection import ASGIConnection

from app.db.config import (JWT_SECRET, JWT_EXPIRES_MIN, JWT_ALG)
from app.db.models.accounts import User
from uuid import UUID
from datetime import timedelta


async def retrieve_user_handler(token: Token, connection:ASGIConnection)-> User:
    return User(id=UUID(token.sub))


jwt_auth = JWTAuth[User](
    token_secret=JWT_SECRET,
    retrieve_user_handler= retrieve_user_handler,
)

def user_access_token(user_id:UUID)-> str:
    return jwt_auth.create_token(
        identifier=str(user_id),
        token_expiration=timedelta(minutes=JWT_EXPIRES_MIN)
    )
    
def decode_token(token: str)-> Token:
    return Token.decode(
        encoded_token=token,
        secret=JWT_SECRET,
        algorithm=JWT_ALG
    )