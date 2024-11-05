from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix='POSTGRES_')

    user: str
    password: str
    db: str
    host: str = 'localhost'
    port: int = 5432


_settings = DBSettings()
connection_url = URL.create(
    'postgresql+psycopg',
    _settings.user,
    _settings.password,
    _settings.host,
    _settings.port,
    _settings.db,
)


class Base(DeclarativeBase):
    pass


engine = create_engine(connection_url)
session = sessionmaker(bind=engine)


def start() -> None:
    Base.metadata.create_all(bind=engine)
