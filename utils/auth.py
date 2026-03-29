# 整合token 查询用户
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import users
from config.db_config import get_db

async def get_current_user(
        authorization: str = Header(...,alias='Authorization'),
        db: AsyncSession = Depends(get_db)):

    token = authorization.split(" ")[0]
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='无效令牌或已过期')
    return user