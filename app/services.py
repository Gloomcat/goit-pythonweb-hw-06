from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete

from app.logger import LOGGER
from app.models import Student, Group, Teacher, Subject, Grade

Tables = Union[Student, Group, Teacher, Subject, Grade]


async def create(session: AsyncSession, table: Tables, **kwargs):
    async with session.begin():
        item = table(**kwargs)
        session.add(item)
        await session.commit()
        LOGGER.info(f"{table.__name__}, created successfully: {kwargs}")


async def remove(session: AsyncSession, table: Tables, id: int):
    async with session.begin():
        await session.execute(delete(table).where(table.id == id))
        LOGGER.info(f"{table.__name__}, ID: {id}, deleted successfully!")


async def update(session: AsyncSession, table: Tables, id: int, **kwargs):
    async with session.begin():
        result = await session.execute(select(table).where(table.id == id))
        item = result.scalars().first()
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            await session.commit()
            LOGGER.info(
                f"{table.__name__} ID {
                        id} updated successfully: {kwargs}"
            )
        else:
            LOGGER.info(f"{table.__name__} ID {id} not found.")


async def list(session: AsyncSession, table: Tables):
    async with session.begin():
        result = await session.execute(select(table))
        items = result.scalars().all()
        for item in items:
            LOGGER.info(
                {
                    column: getattr(item, column)
                    for column in item.__table__.columns.keys()
                }
            )
