from fastapi import FastAPI

from university.services.university import UniversityService
from university.views.university import university_view, auth_view


def new_app(university_service: UniversityService) -> FastAPI:
    app = FastAPI()

    auth_view(app)
    university_view(app, university_service)

    return app
