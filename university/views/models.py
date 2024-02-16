from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from university.services.models import (
    Students,
    Subject,
    RegistrationSubject,
    SubjectApproveResponse,
    SubjectListReject, SubjectListApprove
)


class StudentsDTO(BaseModel):
    id_student: UUID
    name: str
    email: str
    date_of_birth: datetime

    @staticmethod
    def from_student(student: Students):
        return StudentsDTO(
            id_student=student.id_student,
            name=student.name,
            email=student.email,
            date_of_birth=student.date_of_birth
        )


class SubjectInputDTO(BaseModel):
    subject: list[UUID]

    @staticmethod
    def to_service_model(subjects):
        return [Subject(subject) for subject in subjects]


class RegistrationSubjectDTO(BaseModel):
    id_subject: UUID

    @staticmethod
    def from_registration_subject(registration_subject: RegistrationSubject):
        return RegistrationSubjectDTO(
            id_subject=registration_subject.id_subject
        )


class SubjectApproveInputDTO(BaseModel):
    id_subject: UUID
    id_student: UUID
    score: float


class SubjectApproveResponseDTO(BaseModel):
    id_subject: UUID
    id_student: UUID
    score: float
    status: str

    @staticmethod
    def from_finished_subject(subject_finished: SubjectApproveResponse):
        return SubjectApproveResponseDTO(
            id_subject=subject_finished.id_subject,
            id_student=subject_finished.id_student,
            score=subject_finished.score,
            status=subject_finished.status
        )


class SubjectListApproveDTO(BaseModel):
    id_subject: UUID
    id_student: UUID
    score: float
    status: str

    @staticmethod
    def from_subject_passed(subject_passed: SubjectListApprove):
        return SubjectListApproveDTO(
            id_subject=subject_passed.id_subject,
            id_student=subject_passed.id_student,
            score=subject_passed.score,
            status=subject_passed.status,
        )


class SubjectListRejectDTO(BaseModel):
    id_subject: UUID
    id_student: UUID
    score: float
    status: str

    @staticmethod
    def from_subject_reject(subject_reject: SubjectListReject):
        return SubjectListRejectDTO(
            id_subject=subject_reject.id_subject,
            id_student=subject_reject.id_student,
            score=subject_reject.score,
            status=subject_reject.status,
        )
