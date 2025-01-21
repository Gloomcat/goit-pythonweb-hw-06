import pytest
import logging

import app.my_select as queries

from app.logger import LOGGER
from app.database import AsyncSessionLocal
from app.seed import seed_database, verify_tables


@pytest.mark.asyncio
async def test_queries(caplog):
    if not await verify_tables():
        await seed_database()
    assert await verify_tables()

    try:
        session = AsyncSessionLocal()
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
    except Exception as e:
        pytest.fail(e)
