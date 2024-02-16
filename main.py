from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from university.services.university import UniversityService
from app.app import new_app
from app.settings import AppSettings
from university.repositories.university import UniversityRepository


app_settings = AppSettings()

engine = create_async_engine(
    url=str(app_settings.database_settings.dsn),
    pool_size=app_settings.database_settings.pool_size
)
session_maker = async_sessionmaker(bind=engine)

university_repository = UniversityRepository(session_maker)
university_service = UniversityService(university_repository)
app = new_app(university_service)
