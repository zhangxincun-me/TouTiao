import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sympy.polys.polyconfig import query

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from  utils import security

# 根据用户名查询数据库
async def get_user_by_name(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalars().one_or_none()


# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    #先密码加密，---> add
    hashed_password = security.get_hashed_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)  #从数据库读回最新的user
    return user

async def create_token(db: AsyncSession, user_id: int):
    #生成token+设置过期时间，-》查询数据库中是否有Token-> 有：更新; 没有：添加
    token = str(uuid.uuid4())
    expire_at = datetime.now() + timedelta(days=7)
    query= select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expire_at = expire_at
    else:
        user_token = UserToken(user_id=user_id, token=token,expires_at=expire_at)
        db.add(user_token)
    await db.commit()

    return token


# 用户登录校验
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_name(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None

    return user

#根据Token查询用户：验证token--》查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    # 1. 根据token查记录
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    # 2. 检查：不存在 或 已过期
    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


#更新
async def updatw_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
     query = update(User).where(User.username == username).values(**user_data.model_dump(
         exclude_unset=True,
         exclude_none=True
     ))
     result = await db.execute(query)
     await db.commit()

     if result.rowcount == 0:
         return HTTPException(status_code=404, detail="User not found")
     update_user = await get_user_by_name(db, username)
     return update_user


#改密码： 先验证 ---》新密码加密 - ---》修改
async def change_password(db: AsyncSession, user:User,old_password:str,new_password:str):
    if not security.verify_password(old_password, user.password):
        return False

    hashed_password = security.get_hashed_password(new_password)
    user.password = hashed_password
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True













