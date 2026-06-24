from uuid import UUID
from app.db.config import JWT_SECRET,JWT_EXPIRES_MIN, JWT_ALG
from app.authentication import jwt_auth
from datetime import timedelta
from litestar.security.jwt import Token

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