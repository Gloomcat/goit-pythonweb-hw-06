import asyncio

from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)


async def async_main():
    engine = create_async_engine(
        f"postgresql+asyncpg://postgres:1234@postgres:5432/postgres", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with async_session() as session:
        try:
            async with session.begin():
                new_user = User(username="Alice", age=25)
                session.add(new_user)
            print("Transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            print(f"Transaction failed, rolled back. Error: {e}")
