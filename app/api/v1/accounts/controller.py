from litestar import post, get, patch, Request
from litestar.exceptions import HTTPException
from app.api.v1.accounts.security import jwt_auth
from app.db.models.accounts import User, UserRole
from app.api.v1.accounts.service import (
    create_user, 
    authenticate_user,
    user_access_token,
    generate_password_reset_with_token,
    password_reset, update_admin_user)

from app.api.v1.accounts.dto import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    ForgetPassword,
    ResetPassword,
    LoginResponse,
    AdminUserUpdate
)

from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

@post("/auth/register")
async def register_user(
    data: RegisterRequest,
    db_session: AsyncSession
) -> UserResponse:
    try:
        user = await create_user(
            session= db_session,
            email= data.email,
            password_hash= data.password,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        role= user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    

@post("/auth/login")
async def Authenticate_user(
    data: LoginRequest,
    db_session: AsyncSession
) -> LoginResponse:
    try:
        user = await authenticate_user(
            session=db_session,
            email=data.email,
            password=data.password,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invaid username or password")
    token = user_access_token(user.id)
    
    return LoginResponse(
        access_token=token
    )

@post("/auth/password/forget")
async def forget_password(
    data:ForgetPassword,
    db_session: AsyncSession
) -> dict[str, str]:
    try :
        reset_link = await generate_password_reset_with_token(
        session = db_session,
        email = data.email
    )
    except ValueError:
        raise HTTPException(status_code=400, detail="expired token")
    
    return {
        "reset_link": reset_link
    }

@post("/auth/password/reset",)
async def Reset_password(
    data:ResetPassword,
    db_session: AsyncSession
)-> str:
    try:
        await password_reset(
            session = db_session,
            token = data.token,
            new_password=data.new_password,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invaild token")
    
    return "Password reset successful"

@get("/users/me", middleware=[jwt_auth.middleware], security=[{"BearerToken":[]}])
async def Get_user_me(
    request: Request,
    db_session: AsyncSession
)-> UserResponse:
    token_user = request.user
    
    user = await db_session.get(User,token_user.id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return UserResponse(
        id = user.id,
        email = user.email,
        role = user.role,
        is_active = user.is_active,
        created_at= user.created_at,
        updated_at= user.updated_at
    )

@patch("admin/users/{user_id:uuid}", middleware = [jwt_auth.middleware], security=[{"BearerToken":[]}])
async def update_admin(
    user_id: UUID,
    data: AdminUserUpdate,
    request: Request,
    db_session: AsyncSession
)-> UserResponse:
    admin_user = request.user
    user = await db_session.get(User, admin_user.id)
    
    if not user:
        raise HTTPException(status_code= 401, detail="User not found")
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        user = await update_admin_user(
            session = db_session,
            user_id = user_id,
            role = UserRole(data.role),
            is_active = data.is_active
        )
    except ValueError:
        raise HTTPException(status_code= 404, detail="Usernot found")
    return UserResponse(
        id = user.id,
        email = user.email,
        role = user.role,
        is_active= user.is_active,
        created_at= user.created_at,
        updated_at= user.updated_at
    )