from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from app.db.models.accounts import UserRole

@dataclass
class RegisterRequest:
    email: str
    password: str
    
@dataclass
class LoginRequest:
    email: str
    password: str
     
@dataclass
class LoginResponse:
    access_token: str
    
@dataclass
class UserResponse:
    id: UUID
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
@dataclass
class ForgetPassword:
    email: str
    
@dataclass
class ResetPassword:
    token: str
    new_password: str
    
@dataclass
class AdminUserUpdate:
    role: str | None = None
    is_active: bool| None = None