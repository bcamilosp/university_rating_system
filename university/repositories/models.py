from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

from university.services.models import (
    Students,
    RegistrationSubject,
    SubjectListReject,
    SubjectListApprove
)


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(), onupdate=datetime.now())


class StudentsDAO(Base):
    __tablename__ = 'students'

    id_student: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4())
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(nullable=True)

    def to_service_model(self) -> Students:
        return Students(
            id_student=self.id_student,
            name=self.name,
            email=self.email,
            date_of_birth=self.date_of_birth
        )


class SubjectsDAO(Base):
    __tablename__ = 'subjects'
    id_subject: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4())
    name: Mapped[str] = mapped_column(nullable=False)


class RequirementsDAO(Base):
    __tablename__ = 'requirements'
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4())
    id_subject: Mapped[UUID] = mapped_column(ForeignKey(SubjectsDAO.id_subject, ondelete='CASCADE'))
    id_requirement: Mapped[UUID] = mapped_column(ForeignKey(SubjectsDAO.id_subject, ondelete='CASCADE'))


class RegistrationSubjectDAO(Base):
    __tablename__ = 'registration_subject'
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4())
    id_student: Mapped[UUID] = mapped_column(ForeignKey(StudentsDAO.id_student, ondelete='CASCADE'))
    id_subject: Mapped[UUID] = mapped_column(ForeignKey(SubjectsDAO.id_subject, ondelete='CASCADE'))

    def to_service_model(self) -> RegistrationSubject:
        return RegistrationSubject(
            id_subject=self.id_subject
        )


class SubjectApproveDAO(Base):
    __tablename__ = 'subject_approve'
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4())
    id_subject: Mapped[UUID] = mapped_column(ForeignKey(SubjectsDAO.id_subject, ondelete='CASCADE'))
    id_student: Mapped[UUID] = mapped_column(ForeignKey(StudentsDAO.id_student, ondelete='CASCADE'))
    score: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    def to_subject_list_reject(self) -> SubjectListReject:
        return SubjectListReject(
            id_subject=self.id_subject,
            id_student=self.id_student,
            score=self.score,
            status=self.status,
        )

    def to_subject_list_approve(self) -> SubjectListApprove:
        return SubjectListApprove(
            id_subject=self.id_subject,
            id_student=self.id_student,
            score=self.score,
            status=self.status
        )


class UserDAO(Base):
    __tablename__ = 'user'
    id_user: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4())
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
