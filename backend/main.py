from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Project Registry API",
    lifespan=lifespan,
)


@app.get("/api/projects", response_model=list[schemas.ProjectRead])
def list_projects(
    status_filter: Literal["planned", "active", "done"] | None = Query(
        default=None,
        alias="status",
    ),
    db: Session = Depends(get_db),
):
    return crud.list_projects(
        db,
        status=status_filter,
    )


@app.get(
    "/api/projects/{project_id}",
    response_model=schemas.ProjectRead,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = crud.get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project


@app.post(
    "/api/projects",
    response_model=schemas.ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    data: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    return crud.create_project(db, data)


@app.patch(
    "/api/projects/{project_id}",
    response_model=schemas.ProjectRead,
)
def update_project(
    project_id: int,
    data: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = crud.get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return crud.update_project(
        db,
        project,
        data,
    )


@app.delete(
    "/api/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = crud.get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    crud.delete_project(db, project)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )