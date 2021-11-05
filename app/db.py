from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from .config import settings


import sqlalchemy
# по умолчанию вариант
engine  = create_engine('postgresql://postgres:1@localhost:5432/app')


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id: Any
