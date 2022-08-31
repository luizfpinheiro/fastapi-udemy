from typing import Optional

from pydantic import BaseModel, HttpUrl

class ArticleSchema(BaseModel):
    id: Optional[int]
    title: str
    description: str
    url: HttpUrl
    user_id: Optional[id]

    class Config:
        orm_mode = True