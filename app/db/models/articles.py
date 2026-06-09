from uuid import UUID, uuid4
import enum

from sqlalchemy import Enum, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from app.db.models.base import Base

class ArticlesVisibility(str, enum.Enum):
    PUBLIC= 'public'
    PRIVATE = 'private'

class Article(Base):
    __tablename__ = "articles"
    
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] =  mapped_column(Text)
    
    #Fkeys
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"), nullable=False)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    visibility: Mapped[ArticlesVisibility] = mapped_column(Enum(ArticlesVisibility), default=ArticlesVisibility.PUBLIC)
    
    photo_path: Mapped[str] = mapped_column(String(500), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
        #relationships
    category = relationship("Category")
    author = relationship ("User")
