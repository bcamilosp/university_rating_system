from datetime import timedelta
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from Auth.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from university.services.university import UniversityService
from university.views.models import (
    SubjectInputDTO,
    RegistrationSubjectDTO,
    SubjectApproveInputDTO,
    SubjectApproveResponseDTO,
    SubjectListApproveDTO,
    SubjectListRejectDTO
)


def auth_view(app: FastAPI) -> None:
    @app.post("/token", tags=['Auth'])
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


def university_view(app: FastAPI, service: UniversityService) -> None:
    @app.post(
        path='/registration_subjects/{id_student}',
        status_code=status.HTTP_201_CREATED,
        summary='register a subject list',
        response_description='List of subjects',
        tags=['University']
    )
    async def registration_subjects(id_student: UUID, list_id_subject: list[SubjectInputDTO]):
        registration_subject = []
        for subject in list_id_subject:
            list_subject = subject.to_service_model(subject.subject)
            registration_subject.append(await service.registration_subject(id_student, list_subject))
        return registration_subject

    @app.get(
        path='/list_subjects/{id_student}',
        status_code=status.HTTP_200_OK,
        summary='List all subjects for a given student',
        response_description='List of subjects',
        tags=['University']
    )
    async def list_subjects(id_student: UUID):
        list_subject = await service.list_subjects(id_student)
        return [RegistrationSubjectDTO.from_registration_subject(subject) for subject in list_subject]

    @app.post(
        path='/finished_subject/',
        status_code=status.HTTP_201_CREATED,
        summary='List all subjects for a given student',
        response_description='List of subjects',
        tags=['University']
    )
    async def finished_subject(subject_approve_input: SubjectApproveInputDTO):
        subject_finished = await service.finished_subject(subject_approve_input)
        return SubjectApproveResponseDTO.from_finished_subject(subject_finished)

    @app.get(
        path='/approved_subject/{id_student}/',
        status_code=status.HTTP_200_OK,
        summary='List subjects passed',
        response_description='List of subjects',
        tags=['University']
    )
    async def approved_subject(id_student: UUID):
        subject_passed = await service.subject_passed(id_student)
        return [SubjectListApproveDTO.from_subject_passed(reject) for reject in subject_passed]

    @app.get(
        path='/average/{id_student}/',
        status_code=status.HTTP_200_OK,
        summary='average subjects passed',
        response_description='List of average subjects passed',
        tags=['University']
    )
    async def average_subject(id_student: UUID):
        average_passed = await service.average_passed(id_student)
        return average_passed

    @app.get(
        path='/rejected_subject/{id_student}/',
        status_code=status.HTTP_200_OK,
        summary='List subjects reject',
        response_description='List of subjects reject',
        tags=['University']
    )
    async def reject_subject(id_student: UUID):
        subject_reject = await service.subject_reject(id_student)
        return [SubjectListRejectDTO.from_subject_reject(reject) for reject in subject_reject]
