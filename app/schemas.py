from typing import Optional

from pydantic import BaseModel, UUID4
from .models import tasks

# Shared properties
class TaskBase(BaseModel):
    description: Optional[str] = None
    param_1  = "1"
    param_2 = 1


# Properties to receive via API on creation
class TaskCreate(TaskBase):
    description: str
    param_1: str
    param_2: int

# Properties to receive via API on update
class TaskUpdate(TaskBase):
    pass


class TaskInDBBase(TaskBase):
    id: Optional[UUID4] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Task(TaskInDBBase):
    pass


# Additional properties stored in DB
class TaskInDB(TaskInDBBase):
    pass