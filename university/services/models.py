from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Students:
    id_student: UUID
    name: str
    email: str
    date_of_birth: datetime


@dataclass(frozen=True)
class Subject:
    subject: UUID


@dataclass(frozen=True)
class RegistrationSubject:
    id_subject: UUID


@dataclass(frozen=True)
class SubjectApproveResponse:
    id_subject: UUID
    id_student: UUID
    score: float
    status: str



@dataclass(frozen=True)
class SubjectListReject:
    id_subject: UUID
    id_student: UUID
    score: float
    status: str


@dataclass(frozen=True)
class SubjectListApprove:
    id_subject: UUID
    id_student: UUID
    score: float
    status: str


@dataclass(frozen=True)
class SubjectListAverage:
    average: float
