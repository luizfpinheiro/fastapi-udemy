from fastapi import FastAPI

from routes import course_route, user_router

app = FastAPI()
app.include_router(course_route.router, tags=['courses'])
app.include_router(user_router.router, tags=['users'])


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)