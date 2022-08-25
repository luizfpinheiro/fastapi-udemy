from typing import Optional
from pydantic import BaseModel

class Course(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: str
    horas: str


courses = [
    Course(id=1, titulo="Programação para Leigos", aulas=42, horas=56),
    Course(id=2, titulo="Algoritmos e Lógica de Programação", aulas=52, horas=66),
]