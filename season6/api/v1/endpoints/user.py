from typing import List, Optional
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchema, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles
from core.deps import get_session, get_current_user
from core.security import generate_hash
from core.auth import authenticate, create_access_token

router = APIRouter()


@router.get('/logged', response_model=UserSchema)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    """ GET logged user """
    return logged_user


@router.post('signup', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    """ POST user """
    new_user: UserModel = UserModel(
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        is_admin=user.is_admin,
        password=generate_hash(user.password)
    )

    async with db as session:
        session.add(new_user)
        await session.commit()

        return new_user


@router.get('/', response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_session)):
    """ GET all users """
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchema] = result.scalars().all()

        return users


@router.get('/{id}', response_model=List[UserSchemaArticles], status_code=status.HTTP_200_OK)
async def get_user(id: int, db: AsyncSession = Depends(get_session)):
    """ GET user by id with UserSchemaArticles """
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail="User not found.",
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=List[UserSchema], status_code=status.HTTP_200_OK)
async def put_user(id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    """ PUT user by id - with UserSchemaUpdate """
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user_up: UserSchema = result.scalars().unique().one_or_none()

        if user_up:
            if user.name:
                user_up.name = user.name
            if user.lastname:
                user_up.lastname = user.lastname
            if user.email:
                user_up.email = user.email
            if user.is_admin:
                user_up.is_admin = user.is_admin
            if user.senha:
                user_up.senha = generate_hash(user.senha)

            await session.commit()

            return user
        else:
            raise HTTPException(detail="User not found.",
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: AsyncSession = Depends(get_session)):
    """ DELETE user by id """
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user_del: UserSchema = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="User not found.",
                                status_code=status.HTTP_404_NOT_FOUND)


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form.username, password=form.password, db=db)

    if user:
        return JSONResponse(
            content={
                "access_token": create_access_token(sub=user.id),
                "token_type": "bearer"
            }
        )
    else:
        raise HTTPException(detail="Invalid access",
                            status_code=status.HTTP_400_BAD_REQUEST)
