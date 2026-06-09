from dataclasses import dataclass
from uuid import UUID


@dataclass
class RegisterCategory:
    name: str
    slug: str
    
    
@dataclass    
class CategoryResponse:
    id: UUID
    name: str
    slug: str