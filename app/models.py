from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    PrimaryKeyConstraint,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from app.database import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped[list["Grade"]] = relationship(
        "Grade", back_populates="student", cascade="all, delete, delete-orphan"
    )


teacher_subject_association = Table(
    "teacher_subject_association",
    Base.metadata,
    Column("teacher_id", ForeignKey("teachers.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
    PrimaryKeyConstraint("teacher_id", "subject_id"),
)


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", secondary=teacher_subject_association, back_populates="teachers"
    )
    grades: Mapped[list["Grade"]] = relationship(
        "Grade", back_populates="teacher", cascade="all, delete, delete-orphan"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    teachers: Mapped[list["Teacher"]] = relationship(
        "Teacher", secondary=teacher_subject_association, back_populates="subjects"
    )
    grades: Mapped[list["Grade"]] = relationship(
        "Grade", back_populates="subject", cascade="all, delete, delete-orphan"
    )


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE")
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE")
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE")
    )
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    date_received: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="grades")

    @validates("date_received")
    def validate_time(self, _, value):
        if value > datetime.now():
            raise ValueError("Time of grade received must be in the past.")
        return value
