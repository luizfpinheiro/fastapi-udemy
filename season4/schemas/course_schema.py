from typing import Optional
from pydantic import BaseModel as SCBaseModel # Schema Base Model


class CourseSchema(SCBaseModel):
    id: Optional[int]
    titulo: str
    aulas: int
    horas: int

    class Config:
        orm_mode = True

