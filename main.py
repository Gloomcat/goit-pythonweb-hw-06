import asyncio

import app.my_select as queries

from app.database import AsyncSessionLocal
from app.seed import seed_database, verify_tables
from app.logger import LOGGER


async def main():
    if not await verify_tables():
        await seed_database()
    assert await verify_tables()

    async with AsyncSessionLocal() as session:
        await queries.select_1(session)
        await queries.select_2(session)
        await queries.select_3(session)
        await queries.select_4(session)
        await queries.select_5(session)
        await queries.select_6(session)
        await queries.select_7(session)
        await queries.select_8(session)
        await queries.select_9(session)
        await queries.select_10(session)


if __name__ == "__main__":
    asyncio.run(main())
