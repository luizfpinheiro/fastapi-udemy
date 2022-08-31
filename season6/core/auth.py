from pytz import timezone
from typing import Optional, List, EmailStr
from datetime import datetime, timedelta
from fastapi.security import OAuth2AuthorizationCodeBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

# from models import UserModel
from core.configs import settings
from core.security import check_password

oauth2_schema = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)

async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None
        
        if not check_password(password, user.password):
            return None
        
        return user

def _create_token(token_type: str, lifetime: timedelta, subject: str):
    zone = timezone('America/Sao_Paulo')
    expires = datetime.now(tz=zone) + lifetime

    payload = {
        "type": token_type,
        "exp": expires,
        "iat": datetime.now(tz=zone),
        "sub": subject
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_access_token(subject: str) -> str:
    
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        subject=subject
    )
