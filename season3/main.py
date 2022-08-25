from typing import Any, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Response, status, Path, Query
from fastapi.responses import JSONResponse
from models import Course

from time import sleep

app = FastAPI(
    title="Courses API - Geek University",
    version="0.0.1",
    description="API to study FASTApi"
)

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


def fake_db():
    """ Fake function required to execute other functions """
    try:
        print("Connecting database...")
        sleep(1)
    finally:
        print("Closing database connection...")
        sleep(1)


@app.get('/courses', description="Return courses list", summary="Return courses list", response_model=List[Course])
async def get_courses(db: Any = Depends(fake_db)):
    return courses

@app.get('/courses/{id}')
async def get_course(id: int = Path(default=None, title="Course ID"), gt=0, lt=3, db: Any = Depends(fake_db)):
    """Get course by ID"""

    try:
        data = courses[id]
        data["id"] = id
        return data

    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course '{}' not found".format(id))


@app.post("/courses", status_code=status.HTTP_201_CREATED)
async def post_course(course: Course, db: Any = Depends(fake_db)):
    """Create a course object"""
    if course.id not in courses:
        next_id: int = len(courses) + 1
        courses[next_id] = course
        del course.id
        return course
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Course '{}' already exists".format(course.id))


@app.put("/courses/{id}")
async def put_course(id: int, course: Course, db: Any = Depends(fake_db)):
    """Update a course object by ID"""
    if id in courses:
        courses[id] = course
        return course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course '{}' not found".format(id))


@app.delete("/courses/{id}")
async def delete_course(id: int, db: Any = Depends(fake_db)):
    if id in courses:
        del courses[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course '{}' not found".format(id))


@app.get("/calculator")
async def calcular(
    a: int = Query(default=None, gt=5),
    b: int = Query(default=None, gt=10),
    x_geek: str = Header(default=None),
    c: Optional[int] = None
):
    """
    Calculator with 3 parameters
    - a: int greather than 5
    - b: int greather than 10
    - c: int Optional
    """
    soma: int = a + b
    if c:
        soma = soma + c
    print("Header 'X Geek': {}".format(x_geek))

    return {"resultado": soma}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
