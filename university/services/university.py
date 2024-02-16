from typing import List
from uuid import UUID

from university.repositories.university import UniversityRepository
from university.services.models import Subject


class UniversityService:

    def __init__(self, repository: UniversityRepository):
        self.__repository = repository

    async def registration_subject(self, id_student: UUID, list_id_subject: List[Subject]):
        list_subject = {}
        for id_subject in list_id_subject:
            repository = await self.__repository.registration_subject(id_student, id_subject.subject)
            list_subject[id_subject.subject] = repository
        return list_subject

    async def list_subjects(self, id_student: UUID):
        return await self.__repository.list_subjects(id_student)

    async def finished_subject(self, subject_approve_input):
        return await self.__repository.finished_subject(subject_approve_input)

    async def subject_passed(self, id_student: UUID):
        return await self.__repository.subject_passed(id_student)

    async def average_passed(self, id_student: UUID):
        return await self.__repository.average_passed(id_student)

    async def subject_reject(self, id_student: UUID):
        return await self.__repository.subject_reject(id_student)
