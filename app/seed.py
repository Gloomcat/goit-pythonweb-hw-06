from random import randint, choice
from faker import Faker

from app.database import AsyncSessionLocal
from app.models import Student, Group, Teacher, Subject, Grade
from app.logger import LOGGER

fake = Faker()


async def seed_database():
    async with AsyncSessionLocal() as session:
        # Create groups
        try:
            async with session.begin():
                groups = [Group(name=fake.word()) for _ in range(3)]
                session.add_all(groups)
                await session.commit()
            LOGGER.info("Groups transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(
                f"Groups transaction failed, rolled back. Error: {e}")

        # Create teachers
        try:
            async with session.begin():
                teachers = [Teacher(name=fake.name())
                            for _ in range(randint(3, 5))]
                session.add_all(teachers)
                await session.commit()
            LOGGER.info("Teachers transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(
                f"Teachers transaction failed, rolled back. Error: {e}")

        # Create subjects
        try:
            async with session.begin():
                subjects = [
                    Subject(name=fake.word(), teacher=choice(teachers))
                    for _ in range(randint(5, 8))
                ]
                session.add_all(subjects)
                await session.commit()
            LOGGER.info("Subjects transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(
                f"Subjects transaction failed, rolled back. Error: {e}")

        # Create students
        try:
            async with session.begin():
                students = [
                    Student(name=fake.name(), group=choice(groups))
                    for _ in range(randint(30, 50))
                ]
                session.add_all(students)
                await session.commit()
            LOGGER.info("Students transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(
                f"Students transaction failed, rolled back. Error: {e}")

        # Assign grades
        try:
            async with session.begin():
                grades = []
                for student in students:
                    for subject in subjects:
                        for _ in range(randint(10, 20)):
                            grades.append(
                                Grade(
                                    student=student,
                                    subject=subject,
                                    grade=randint(1, 100),
                                    date_received=fake.date_time_this_year(),
                                )
                            )
                session.add_all(grades)
                await session.commit()
            LOGGER.info("Students transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(
                f"Students transaction failed, rolled back. Error: {e}")

    LOGGER.info("Database seeding finished")
