from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_model import CourseModel
from schemas.course_schema import CourseSchema
from core.deps import get_session

router = APIRouter()

# POST Course


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def post_course(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(titulo=course.titulo,
                             aulas=course.aulas, horas=course.horas)

    db.add(new_course)
    await db.commit()

    return new_course


@router.get('/', response_model=List[CourseSchema])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()

        return courses


@router.get('/{id}', response_model=CourseSchema, status_code=status.HTTP_200_OK)
async def get_course(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(detail="Course not found.",
                                status_code=status.HTTP_404_NOT_FOUND)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=CourseSchema)
async def put_course(id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == id)
        result = await session.execute(query)
        course_up = result.scalar_one_or_none()

        if course_up:
            course_up.titulo = course.titulo
            course_up.aulas = course.aulas
            course_up.horas = course.horas

            await session.commit()

            return course_up
        else:
            raise HTTPException(detail="Course not found.",
                                status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == id)
        result = await session.execute(query)
        course_del = result.scalar_one_or_none()

        if course_del:
            await session.delete(course_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Course not found.",
                                status_code=status.HTTP_404_NOT_FOUND)                                