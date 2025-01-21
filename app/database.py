from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/postgres"

AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=AsyncEngine, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
