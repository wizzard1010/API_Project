from uuid import UUID, uuid4
import enum
from sqlalchemy import Boolean, Enum, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from app.db.models.base import Base

class UserRole(str, enum.Enum):
    USER = 'user'
    ADMIN = 'admin'
    AUTHOR = 'author'

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    