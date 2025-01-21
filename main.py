import asyncio
import argparse

from app.database import AsyncSessionLocal
from app.services import create, update, list, remove
from app.models import NAME_TO_TABLE
from app.logger import LOGGER


async def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for database management")
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["Teacher", "Group", "Student", "Subject", "Grade"],
        required=True,
        help="Database model",
    )
    parser.add_argument("-n", "--name", type=str, help="Name of the entity")
    parser.add_argument("-g", "--grade", type=int, help="Grade for the entity")
    parser.add_argument(
        "--id", type=int, help="ID of the entity to update or remove")

    parser.add_argument(
        "-stid",
        "--student-id",
        type=int,
        help="ID of the student entity to add relation for",
    )
    parser.add_argument(
        "-sid",
        "--subject-id",
        type=int,
        help="ID of the subject entity to add relation for",
    )
    parser.add_argument(
        "-gid",
        "--group-id",
        type=int,
        help="ID of the group entity to add relation for",
    )
    parser.add_argument(
        "-tid",
        "--teacher-id",
        type=int,
        help="ID of the teacher entity to add relation for",
    )

    args = parser.parse_args()

    try:
        async with AsyncSessionLocal() as session:
            if args.model in NAME_TO_TABLE:
                model = NAME_TO_TABLE[args.model]
                kwargs = {
                    k: v
                    for k, v in vars(args).items()
                    if v is not None and k not in ["action", "model", "id"]
                }

                if args.action == "create" and (args.name or args.grade):
                    await create(session, model, **kwargs)
                elif args.action == "update" and args.id:
                    await update(session, model, args.id, **kwargs)
                elif args.action == "list":
                    await list(session, model)
                elif args.action == "remove" and args.id:
                    await remove(session, model, args.id)
            else:
                LOGGER.warning(f"Model {args.model} not yet implemented.")
    except Exception as e:
        LOGGER.critical(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
