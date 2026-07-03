import asyncio
from uuid import UUID
from datetime import datetime
from app.db.models.category import Category
from app.db.models.accounts import User

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import delete
from app.db.models.articles import Article, ArticlesVisibility


DATABASE_URL = "postgresql+asyncpg://james:james123@db:5432/api_db"

ADMIN_ID = UUID("0fcf018c-8d54-4c8e-bc1a-17e46068daa3")
WEB_DEVELOPMENT_CATEGORY_ID = UUID("01b8778d-40f2-4060-b0c6-ea3829799ea3")


articles_data = [
    {
        "title": "Getting Started With Backend APIs",
        "body": "This article explains backend API development using Python, Litestar, PostgreSQL, and SQLAlchemy.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/backend-api.jpg",
    },
    {
        "title": "JWT Authentication Basics",
        "body": "This article explains login, access tokens, bearer tokens, Authorization headers, and protected API routes.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/jwt-auth.jpg",
    },
    {
        "title": "Private Admin API Notes",
        "body": "This private article contains internal notes about admin routes, user roles, and permission checks.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/admin-notes.jpg",
    },
    {
        "title": "Building REST APIs With Litestar",
        "body": "This article introduces routing, controllers, handlers, services, and response DTOs in Litestar.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/litestar-api.jpg",
    },
    {
        "title": "SQLAlchemy Async Session Guide",
        "body": "This article explains AsyncSession, select queries, commits, refresh, and database transactions.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/sqlalchemy.jpg",
    },
    {
        "title": "Private Database Migration Plan",
        "body": "This private article contains internal notes about Alembic migrations and future schema changes.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/migration-plan.jpg",
    },
    {
        "title": "PostgreSQL Search Testing",
        "body": "This article is used to test search, pagination, title matching, and body matching in PostgreSQL.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/postgres-search.jpg",
    },
    {
        "title": "Docker Compose for API Projects",
        "body": "This article explains how to run an API and PostgreSQL database together using Docker Compose.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/docker-compose.jpg",
    },
    {
        "title": "Private Deployment Checklist",
        "body": "This private article contains internal deployment checklist items for API release preparation.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/deployment-checklist.jpg",
    },
    {
        "title": "Article Visibility Rules Explained",
        "body": "This article explains public and private article visibility for anonymous and authenticated users.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/visibility-rules.jpg",
    },
    {
        "title": "API Error Handling Guide",
        "body": "This article explains HTTP status codes, exceptions, validation errors, and clean error responses.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/error-handling.jpg",
    },
    {
        "title": "Pagination in API Design",
        "body": "This article explains page, page_size, limit, offset, and how pagination works in API endpoints.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/pagination.jpg",
    },
    {
        "title": "Private API Refactor Notes",
        "body": "This private article contains internal refactor notes for services, controllers, DTOs, and helpers.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/api-refactor.jpg",
    },
    {
        "title": "User Role Management",
        "body": "This article explains user roles such as user, author, admin, and how permissions are checked.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/user-roles.jpg",
    },
    {
        "title": "Testing API Endpoints With Postman",
        "body": "This article explains how to test GET, POST, PATCH, DELETE, headers, tokens, and JSON bodies.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/postman-testing.jpg",
    },
    {
        "title": "Private Security Review",
        "body": "This private article contains internal security review notes about JWT secrets, tokens, and access control.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/security-review.jpg",
    },
    {
        "title": "Git Workflow for API Projects",
        "body": "This article explains git add, commit, push, pull rebase, branches, and clean commit messages.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/git-workflow.jpg",
    },
    {
        "title": "Docker Logs and Debugging",
        "body": "This article explains how to check API logs, database logs, container status, and debugging errors.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/docker-logs.jpg",
    },
    {
        "title": "Async Python for Backend Development",
        "body": "This article explains async and await, event loops, database calls, and non-blocking API code.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/async-python.jpg",
    },
    {
        "title": "Private JWT Debug Notes",
        "body": "This private article contains internal debugging notes for token decode errors and Authorization headers.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/jwt-debug.jpg",
    },
    {
        "title": "Database Relationships Explained",
        "body": "This article explains foreign keys, authors, categories, relationships, and joined data in SQLAlchemy.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/db-relationships.jpg",
    },
    {
        "title": "Alembic Migration Basics",
        "body": "This article explains how Alembic tracks database schema changes and applies migration files.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/alembic.jpg",
    },
    {
        "title": "Private Release Planning Notes",
        "body": "This private article contains internal release planning notes for the next backend API version.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/release-plan.jpg",
    },
    {
        "title": "Clean Controller and Service Structure",
        "body": "This article explains separating controller logic, service logic, DTOs, helpers, and database models.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/clean-structure.jpg",
    },
    {
        "title": "API Search Endpoint Design",
        "body": "This article explains how to build search endpoints using query text, filters, visibility, and pagination.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/search-endpoint.jpg",
    },
    {
        "title": "Private Search Optimization Notes",
        "body": "This private article contains internal notes about search performance, indexes, and future improvements.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/search-optimization.jpg",
    },
    {
        "title": "PostgreSQL Indexing Introduction",
        "body": "This article explains indexes, unique constraints, search speed, and query optimization basics.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/postgres-index.jpg",
    },
    {
        "title": "Environment Variables in Docker",
        "body": "This article explains environment variables, secrets, database URLs, JWT settings, and Docker configuration.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/env-vars.jpg",
    },
    {
        "title": "Private Production Security Checklist",
        "body": "This private article contains internal security checklist items before deploying the API to production.",
        "visibility": ArticlesVisibility.PRIVATE,
        "photo_path": "/uploads/articles/production-security.jpg",
    },
    {
        "title": "Backend Project Final Review",
        "body": "This article reviews authentication, authorization, categories, articles, search, pagination, and deployment preparation.",
        "visibility": ArticlesVisibility.PUBLIC,
        "photo_path": "/uploads/articles/final-review.jpg",
    },
]


async def main() -> None:
    engine = create_async_engine(DATABASE_URL)
    db_session = async_sessionmaker(engine, expire_on_commit=False)

    async with db_session() as session:
        articles = []

        for a in articles_data:
            article = Article(
                title=a["title"],
                body=a["body"],
                category_id=WEB_DEVELOPMENT_CATEGORY_ID,
                author_id=ADMIN_ID,
                visibility=a["visibility"],
                photo_path=a["photo_path"],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            articles.append(article)

        await session.execute(delete(Article))
        session.add_all(articles)
        await session.commit()

    await engine.dispose()

    print(f"Seeded {len(articles_data)} articles successfully.")


if __name__ == "__main__":
    asyncio.run(main())