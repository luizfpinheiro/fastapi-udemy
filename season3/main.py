from os import stat
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse

from models import Course
from typing import List, Optional

app = FastAPI()

courses = {
    1: {
        "titulo": "Programação para Leigos",
        "aulas": 112,
        "horas": 58
    },
    2: {
        "titulo": "Algoritmos e Lógica de Programação",
        "aulas": 87,
        "horas": 67
    }
}


@app.get('/courses')
async def get_courses():
    """Courses List"""
    return courses


@app.get('/courses/{id}')
async def get_course(id: int):
    """Get course by ID"""

    try:
        data = courses[id]
        data["id"] = id
        return data

    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course '{}' not found".format(id))


@app.post("/courses", status_code=status.HTTP_201_CREATED)
async def post_course(course: Course):
    if course.id not in courses:
        next_id: int = len(courses) + 1
        courses[next_id] = course
        del course.id
        return course
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Course '{}' already exists".format(course.id))


@app.put("/courses/{id}")
async def put_course(id: int, course: Course):
    if id in courses:
        courses[id] = course
        return course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course '{}' not found".format(id))

@app.delete("/courses/{id}")
async def delete_course(id: int):
    if id in courses:
        del courses[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course '{}' not found".format(id))

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
