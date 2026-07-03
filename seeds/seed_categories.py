import asyncio
from uuid import UUID
from datetime import datetime
from app.db.models.category import Category
from app.db.models.accounts import User
from sqlalchemy import delete



from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://james:james123@db:5432/api_db"

categories_data = [
  { "name": "Technology", "slug": "technology" },
  { "name": "Programming", "slug": "programming" },
  { "name": "Software Engineering", "slug": "software-engineering" },
  { "name": "Web Development", "slug": "web-development" },
  { "name": "Mobile Development", "slug": "mobile-development" },
  { "name": "Frontend", "slug": "frontend" },
  { "name": "Backend", "slug": "backend" },
  { "name": "DevOps", "slug": "devops" },
  { "name": "Cloud Computing", "slug": "cloud-computing" },
  { "name": "Cybersecurity", "slug": "cybersecurity" },
  { "name": "Artificial Intelligence", "slug": "artificial-intelligence" },
  { "name": "Machine Learning", "slug": "machine-learning" },
  { "name": "Data Science", "slug": "data-science" },
  { "name": "Data Engineering", "slug": "data-engineering" },
  { "name": "Databases", "slug": "databases" },
  { "name": "Open Source", "slug": "open-source" },
  { "name": "Linux", "slug": "linux" },
  { "name": "Networking", "slug": "networking" },
  { "name": "System Design", "slug": "system-design" },
  { "name": "Architecture", "slug": "architecture" },
  { "name": "Testing", "slug": "testing" },
  { "name": "Automation", "slug": "automation" },
  { "name": "API Development", "slug": "api-development" },
  { "name": "Microservices", "slug": "microservices" },
  { "name": "Containers", "slug": "containers" },
  { "name": "Kubernetes", "slug": "kubernetes" },
  { "name": "Blockchain", "slug": "blockchain" },
  { "name": "Internet of Things", "slug": "internet-of-things" },
  { "name": "Game Development", "slug": "game-development" },
  { "name": "Career", "slug": "career" }
]

async def main()-> None:
    engine = create_async_engine(DATABASE_URL)
    db_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with db_session()as session:
        categories = []
        for c in categories_data:
            category = Category(
                name = c["name"],
                slug = c["slug"]
            )
            categories.append(category)
        
        await session.execute(delete(Category))
        session.add_all(categories)
        await session.commit()
    
    await engine.dispose()
    print(f"Seeded{len(categories_data)} categories successfully.")
    
if __name__ =="__main__":
    asyncio.run(main())