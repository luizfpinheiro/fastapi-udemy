from typing import Optional, List
from pydantic import BaseModel, EmailStr
from schemas.article_schema import ArticleSchema

class UserSchema(BaseModel):
    id: Optional[int]
    name = Optional[str]
    lastname = Optional[str]
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True

class UserSchemaCreate(UserSchema):
    password: str

class UserSchemaArticles(UserSchema):
    articles: Optional[List[ArticleSchema]]

class UserSchemaUpdate(UserSchema):
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    password = Optional[str]
    is_admin: bool = Optional[str]

