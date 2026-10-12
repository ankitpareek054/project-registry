from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ProjectStatus = Literal[
    "planned",
    "active",
    "done",
]


class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=120,
    )

    description: str = Field(
        default="",
        max_length=1000,
    )

    status: ProjectStatus = "planned"


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    status: ProjectStatus | None = None


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    status: ProjectStatus

    model_config = ConfigDict(
        from_attributes=True
    )