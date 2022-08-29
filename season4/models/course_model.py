from core.configs import settings
from sqlalchemy import Column, Integer, String

class CourseModel(settings.DB_BASE_MODEL):
    __tablename__ = 'courses'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    titulo: str = Column(String(100))
    aulas: int = Column(Integer)
    horas: int = Column(Integer)