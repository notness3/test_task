from typing import Any, List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from . import actions, models, schemas
from .db import SessionLocal, engine

# Create all tables in the database.
# Comment this out if you using migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get DB session.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"message": "Hello world!"}


@app.get("/tasks", response_model=List[schemas.Task], tags=["tasks"])
def list_tasks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    tasks = actions.tasks.get_all(db=db, skip=skip, limit=limit)
    return tasks


@app.post(
    "/tasks", response_model=schemas.Task, status_code=HTTP_201_CREATED, tags=["tasks"]
)
def create_task(*, db: Session = Depends(get_db), post_in: schemas.TaskCreate) -> Any:
    tasks = actions.tasks.create(db=db, obj_in=post_in)
    return tasks


@app.put(
    "/tasks/{id}",
    response_model=schemas.Task,
    #responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["tasks"],
)
def update_task(
    *, db: Session = Depends(get_db), id: UUID4, task_in: schemas.TaskUpdate,
) -> Any:
    tasks = actions.tasks.get(db=db, id=id)
    if not tasks:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
    tasks = actions.tasks.update(db=db, db_obj=tasks, obj_in=task_in)
    return tasks


@app.get(
    "/tasks/{id}",
    response_model=schemas.Task,
    #responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["tasks"],
)
def get_task(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    tasks = actions.tasks.get(db=db, id=id)
    if not tasks:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
    return  tasks


@app.delete(
    "/tasks/{id}",
    response_model=schemas.Task,
    #responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["tasks"],
)
def delete_task(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    tasks = actions.tasks.get(db=db, id=id)
    if not tasks:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found")
    tasks = actions.tasks.remove(db=db, id=id)
    return tasks