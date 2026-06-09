from dataclasses import dataclass
from uuid import UUID

@dataclass
class CreateArticle:
    title: str
    body: str
    category_id: UUID
    author_id: UUID
    photo_path: str
    
@dataclass
class ArticleResponse:
    id: UUID
    title: str
    body: str
    category_id:UUID
    author_id: UUID
    photo_path: str
    
    
