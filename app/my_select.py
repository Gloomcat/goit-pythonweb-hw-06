from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from random import choice

from app.models import (
    Student,
    Group,
    Teacher,
    Subject,
    Grade,
    teacher_subject_association,
)
from app.logger import LOGGER


async def select_1(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(
            select(Student.name, func.avg(Grade.grade).label("avg_grade"))
            .join(Grade)
            .group_by(Student.id, Student.name)
            .order_by(func.avg(Grade.grade).desc())
            .limit(5)
        )
        students = result.all()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info("Top 5 students by average grade:")
        for student, avg_grade in students:
            LOGGER.info(f"Student: '{student}', Avg. grade: '{avg_grade}'")
        LOGGER.info("--------------------------------------------------------")


async def select_2(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Subject))
        subject = choice(result.scalars().all())
        result = await session.execute(
            select(Student.name, func.avg(Grade.grade).label("avg_grade"))
            .join(Grade)
            .join(Subject)
            .where(Subject.id == subject.id)
            .group_by(Student.id, Student.name)
            .order_by(func.avg(Grade.grade).desc())
            .limit(1)
        )
        student, avg_grade = result.first()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(
            f"Student with highest average grade on subject '{
                subject.name}':"
        )
        LOGGER.info(f"Student: '{student}', Avg. grade: '{avg_grade}'")
        LOGGER.info("--------------------------------------------------------")


async def select_3(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Subject))
        subject = choice(result.scalars().all())
        result = await session.execute(
            select(Group.name, func.avg(Grade.grade).label("avg_grade"))
            .select_from(Group)
            .join(Student, Group.id == Student.group_id)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Subject.id == Grade.subject_id)
            .where(Subject.id == subject.id)
            .group_by(Group.id, Group.name)
        )
        groups = result.all()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(f"Groups with average grades on subject '{subject.name}':")
        for group, avg_grade in groups:
            LOGGER.info(f"Group: '{group}', Avg. grade: '{avg_grade}'")
        LOGGER.info("--------------------------------------------------------")


async def select_4(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(
            select(func.avg(Grade.grade).label("overall_avg"))
        )
        overall_avg = result.scalar()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(f"Overall average grade: '{overall_avg}':")
        LOGGER.info("--------------------------------------------------------")


async def select_5(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Teacher))
        teacher = choice(result.scalars().all())
        result = await session.execute(
            select(Subject.name)
            .join(
                teacher_subject_association,
                teacher_subject_association.c.subject_id == Subject.id,
            )
            .where(teacher_subject_association.c.teacher_id == teacher.id)
        )
        courses = result.scalars().all()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(f"Courses taught by '{teacher.name}': {courses}")
        LOGGER.info("--------------------------------------------------------")


async def select_6(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Group))
        group = choice(result.scalars().all())
        result = await session.execute(
            select(Student.name).join(Group).where(Group.name == group.name)
        )
        students = result.scalars().all()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(f"Students in group '{group.name}': {students}")
        LOGGER.info("--------------------------------------------------------")


async def select_7(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Subject))
        subject = choice(result.scalars().all())
        result = await session.execute(select(Group))
        group = choice(result.scalars().all())
        result = await session.execute(
            select(Student.name, Grade.grade)
            .join(Grade)
            .where(Student.group_id == group.id, Grade.subject_id == subject.id)
            .order_by(Student.name.asc())
        )
        students = result.all()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(
            f"Students' grades from group '{
                group.name}' on subject '{subject.name}':"
        )
        for student, grade in students:
            LOGGER.info(f"Student: '{student}', Grade: '{grade}'")
        LOGGER.info("--------------------------------------------------------")


async def select_8(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Teacher))
        teacher = choice(result.scalars().all())
        result = await session.execute(
            select(Subject.name, func.avg(Grade.grade).label("avg_grade"))
            .join(
                teacher_subject_association,
                teacher_subject_association.c.subject_id == Subject.id,
            )
            .join(Grade)
            .where(
                teacher_subject_association.c.teacher_id == teacher.id,
                Grade.subject_id == teacher_subject_association.c.subject_id,
            )
            .group_by(Subject.id, Subject.name)
        )

        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(
            f"Average grades for subjects by teacher '{
                teacher.name}':"
        )
        subjects = result.all()
        for subject, grade in subjects:
            LOGGER.info(f"Subject: '{subject}', Grade: '{grade}'")
        LOGGER.info("--------------------------------------------------------")


async def select_9(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Student))
        student = choice(result.scalars().all())
        result = await session.execute(
            select(Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .where(Grade.student_id == student.id)
            .group_by(Subject.id, Subject.name)
        )
        subjects = result.scalars().all()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(f"Student '{student.name}' attends subjects: {subjects}")
        LOGGER.info("--------------------------------------------------------")


async def select_10(session: AsyncSession) -> None:
    async with session.begin():
        result = await session.execute(select(Student))
        student = choice(result.scalars().all())
        result = await session.execute(select(Teacher))
        teacher = choice(result.scalars().all())
        result = await session.execute(
            select(Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .where(Grade.student_id == student.id, Grade.teacher_id == teacher.id)
            .group_by(Subject.id, Subject.name)
        )
        subjects = result.scalars().all()
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info(
            f"Student '{student.name}' attends subjects: {
                subjects}, taught by teacher '{teacher.name}'"
        )
        LOGGER.info("--------------------------------------------------------")
