from typing import Optional
from pydantic import BaseModel, validator


class Course(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: str
    horas: str

    @validator('titulo')
    def validate_titulo(cls, value):
        # Check if 'titulo' has at least three words
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError("'titulo' must be have three words.")

        # Check if 'titulo' is capitalize
        if value.islower():
            raise ValueError("'titulo' must be capitalize.")

        return value

    @validator('aulas')
    def validate_aulas(cls, value):

        if int(value) < 12:
            raise ValueError("'aulas' must be greather or equal than 12.")

        return value

    @validator('horas')
    def validate_horas(cls, value):

        if int(value) < 10:
            raise ValueError("'horas' must be greather or equal than 10.")

        return value


courses = [
    Course(id=1, titulo="Programação para Leigos", aulas=42, horas=56),
    Course(id=2, titulo="Algoritmos e Lógica de Programação", aulas=52, horas=66),
]
