import asyncio

from app.database import AsyncSessionLocal
from app.models import User


async def async_main():
    async with AsyncSessionLocal() as session:
        try:
            async with session.begin():
                new_user = User(username="Alice", age=25)
                session.add(new_user)
            print("Transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            print(f"Transaction failed, rolled back. Error: {e}")


if __name__ == "__main__":
    asyncio.run(async_main())
