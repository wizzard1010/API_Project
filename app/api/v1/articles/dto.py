from dataclasses import dataclass
from uuid import UUID
from app.db.models.articles import ArticlesVisibility
@dataclass
class CreateArticle:
    title: str
    body: str
    category_id: UUID
    author_id: UUID
    #photo_path: str
    visibility: ArticlesVisibility = ArticlesVisibility.PUBLIC
    
@dataclass
class ArticleResponse:
    id: UUID
    title: str
    body: str
    category_id:UUID
    author_id: UUID
    photo_path: str
    visibility: ArticlesVisibility

@dataclass
class ArticleUpdate:
    title: str
    body:str
    visibility: ArticlesVisibility

