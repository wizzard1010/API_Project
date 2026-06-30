from typing import Optional
from litestar import Request
from app.api.v1.accounts.security import decode_token
from uuid import UUID
from app.db.models.accounts import User
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_from_header(
    request: Request,
    db_session: AsyncSession,
) -> Optional[User]:
    auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "", 1)
    
        try:
            decoded_token = decode_token(token)
            user_id = UUID(decoded_token.sub)
        
            user = await db_session.get(User, user_id)
            
            return user
        except Exception:
            return None
        
            