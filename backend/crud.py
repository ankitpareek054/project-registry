from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Project
from .schemas import ProjectCreate, ProjectUpdate


def list_projects(
    db: Session,
    status: str | None = None,
):
    statement = select(Project).order_by(Project.id)

    if status is not None:
        statement = statement.where(
            Project.status == status
        )

    return db.scalars(statement).all()


def get_project(
    db: Session,
    project_id: int,
):
    return db.get(Project, project_id)


def create_project(
    db: Session,
    data: ProjectCreate,
):
    project = Project(
        **data.model_dump()
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def update_project(
    db: Session,
    project: Project,
    data: ProjectUpdate,
):
    changes = data.model_dump(
        exclude_unset=True
    )

    for field, value in changes.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project: Project,
):
    db.delete(project)
    db.commit()