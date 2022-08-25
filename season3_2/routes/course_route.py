from fastapi import APIRouter

router = APIRouter()

@router.get('/api/v1/courses')
async def get_cursos():
    return {"info": "success!"}