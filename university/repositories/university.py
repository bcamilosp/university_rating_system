from uuid import UUID

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from university.constans import APPROVED, REJECTED
from university.repositories.models import (
    RegistrationSubjectDAO,
    RequirementsDAO,
    SubjectApproveDAO,
    UserDAO
)


class UniversityRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.__session_maker = session_maker

    async def registration_subject(self, id_student, id_subject):
        async with self.__session_maker() as session:
            async with session.begin():
                query_init = select(RequirementsDAO).where(RequirementsDAO.id_subject == id_subject)
                result_query_init = await session.execute(query_init)
                validation_requirements = result_query_init.scalar()
                if validation_requirements is True:
                    query = select(
                        RequirementsDAO,
                        SubjectApproveDAO,
                    ).join(
                        SubjectApproveDAO,
                        SubjectApproveDAO.id_subject == RequirementsDAO.id_requirement
                    ).where(and_(SubjectApproveDAO.id_student == id_student,
                                 RequirementsDAO.id_subject == id_subject)).filter(
                        SubjectApproveDAO.status == APPROVED)
                    result = await session.execute(query)
                    registration_dao = result.scalar()
                    if registration_dao:
                        registration_dao = RegistrationSubjectDAO(
                                id_student=id_student,
                                id_subject=id_subject,
                        )
                        session.add(registration_dao)
                        await session.flush()
                        await session.refresh(registration_dao)
                        return "properly registered subject"
                    return "missing requirement subjects"
                registration_without_requirements_dao = RegistrationSubjectDAO(
                    id_student=id_student,
                    id_subject=id_subject,
                )
                session.add(registration_without_requirements_dao)
                await session.flush()
                await session.refresh(registration_without_requirements_dao)
                return "properly registered subject"

    async def list_subjects(self, id_student: UUID):
        async with self.__session_maker() as session:
            async with session.begin():
                query = select(RegistrationSubjectDAO).where(RegistrationSubjectDAO.id_student == id_student)
                subjects_dao = await session.execute(query)
                await session.close()
                return [registration_subject.to_service_model() for registration_subject in subjects_dao.scalars()]

    async def finished_subject(self, subject_approve_input):
        async with self.__session_maker() as session:
            async with session.begin():
                query = select(RegistrationSubjectDAO).where(
                    RegistrationSubjectDAO.id_student == subject_approve_input.id_student,
                    RegistrationSubjectDAO.id_subject == subject_approve_input.id_subject
                )
                result = await session.execute(query)
                subject_registered = result.scalar()
                if subject_registered:
                    await session.delete(subject_registered)
                    await session.flush()
                subject_approve = SubjectApproveDAO(
                    id_student=subject_approve_input.id_student,
                    id_subject=subject_approve_input.id_subject,
                    score=subject_approve_input.score,
                    status=APPROVED if subject_approve_input.score >= 3.0 else REJECTED
                )
                session.add(subject_approve)
                await session.flush()
                await session.refresh(subject_approve)
                await session.close()
                return subject_approve

    async def subject_passed(self, id_student):
        async with self.__session_maker() as session:
            async with session.begin():
                query = select(SubjectApproveDAO).where(
                    SubjectApproveDAO.id_student == id_student,
                    SubjectApproveDAO.status == APPROVED
                )
                result = await session.execute(query)
                await session.close()
                return [subject.to_subject_list_approve() for subject in result.scalars()]

    async def average_passed(self, id_student):
        async with self.__session_maker() as session:
            async with session.begin():
                query = select(func.avg(SubjectApproveDAO.score).label('average')).where(
                    SubjectApproveDAO.id_student == id_student
                )
                result = await session.execute(query)
                average = result.scalar()
                return average

    async def subject_reject(self, id_student):
        async with self.__session_maker() as session:
            async with session.begin():
                query = select(SubjectApproveDAO).where(
                    SubjectApproveDAO.id_student == id_student,
                    SubjectApproveDAO.status == REJECTED)
                result = await session.execute(query)
                await session.close()
                return [subject.to_subject_list_reject() for subject in result.scalars()]

    async def get_user(self, username):
        async with self.__session_maker() as session:
            async with session.begin():
                query = select(UserDAO).where(UserDAO.username == username)
                result = await session.execute(query)
                return result
