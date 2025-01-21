from random import randint, choice, sample
from faker import Faker
from faker.providers import DynamicProvider
from sqlalchemy.sql import select

from app.database import AsyncSessionLocal
from app.logger import LOGGER
from app.models import (
    Student,
    Group,
    Teacher,
    Subject,
    Grade,
    teacher_subject_association,
)

fake = Faker()

# Define subject and group providers
subjects_provider = DynamicProvider(
    provider_name="subject_name",
    elements=[
        "Mathematics",
        "Physics",
        "CS",
        "Biology",
        "History",
        "Geography",
        "Literature",
        "Economics",
        "Psychology",
        "Philosophy",
        "Political Science",
    ],
)

groups_provider = DynamicProvider(
    provider_name="group_name",
    elements=[f"Group {i}" for i in range(1, 10)],
)

fake.add_provider(subjects_provider)
fake.add_provider(groups_provider)


async def seed_database():
    async with AsyncSessionLocal() as session:
        try:
            # Create groups
            groups = [Group(name=fake.unique.group_name()) for _ in range(3)]
            session.add_all(groups)
            await session.commit()
            LOGGER.info("Groups transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(f"Groups transaction failed, rolled back. Error: {e}")

        try:
            # Create teachers
            teachers = [Teacher(name=fake.unique.name()) for _ in range(randint(3, 5))]
            session.add_all(teachers)
            await session.commit()
            LOGGER.info("Teachers transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(f"Teachers transaction failed, rolled back. Error: {e}")

        try:
            # Create subjects
            subjects = [
                Subject(name=fake.unique.subject_name()) for _ in range(randint(5, 8))
            ]
            session.add_all(subjects)
            await session.commit()
            LOGGER.info("Subjects transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(f"Subjects transaction failed, rolled back. Error: {e}")

        # Assign multiple teachers to subjects in the association table
        for subject in subjects:
            assigned_teachers = sample(teachers, randint(1, min(3, len(teachers))))
            for teacher in assigned_teachers:
                await session.execute(
                    teacher_subject_association.insert().values(
                        teacher_id=teacher.id, subject_id=subject.id
                    )
                )
        LOGGER.info("Teacher-Subject associations committed successfully.")

        try:
            # Create students and assign them to a random group
            students = [
                Student(name=fake.unique.name(), group=choice(groups))
                for _ in range(randint(30, 50))
            ]
            session.add_all(students)
            await session.commit()
            LOGGER.info("Students transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(f"Students transaction failed, rolled back. Error: {e}")

        try:
            # Assign grades to students for their subjects
            grades = []
            for student in students:
                for subject in subjects:
                    result = await session.execute(
                        select(Teacher)
                        .join(teacher_subject_association)
                        .where(teacher_subject_association.c.subject_id == subject.id)
                    )
                    subject_teachers = result.scalars().all()
                    if subject_teachers:
                        # Choose one teacher from assigned teachers
                        teacher = choice(subject_teachers)
                        for _ in range(randint(10, 20)):
                            grades.append(
                                Grade(
                                    student=student,
                                    subject=subject,
                                    teacher=teacher,
                                    grade=randint(1, 100),
                                    date_received=fake.date_time_this_year(),
                                )
                            )
            session.add_all(grades)
            await session.commit()
            LOGGER.info("Grades transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            LOGGER.warning(f"Grades transaction failed, rolled back. Error: {e}")

    LOGGER.info("Database seeding finished")


async def verify_tables():
    async with AsyncSessionLocal() as session:
        tables = {Group, Student, Teacher, Subject, Grade, teacher_subject_association}
        for table in tables:
            result = await session.execute(select(table))
            values = result.scalars().all()
            if not values:
                return False
        return True
