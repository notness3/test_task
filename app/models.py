from uuid import uuid4
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from .db import Base


class tasks(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    description = Column(String)
    param_1 = Column(String)
    param_2 = Column(Integer)
