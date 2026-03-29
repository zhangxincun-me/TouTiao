from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_config import get_db
from crud import users
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest
from utils.response import success_response
from utils.auth import get_current_user
from models.users import User, UserChangePasswordRequest

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑 ：验证用户是否存在--》创建用户--》生成Token-->响应结果
    existing_user = await users.get_user_by_name(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    # return {
    #     "code": 200,
    #     "message": "success",
    #     "data": {
    #         "token": token,
    #         "userinfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar,
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    #验证用户是否存在 ---》 验证密码  ---》 生成Token ---》 响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=response_data)


@router.get("/info")
async def info(user: User = Depends(get_current_user)):
    return success_response(message='获取用户信息成功',data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update(
        user_data: UserUpdateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    user = await users.updatw_user(db,user.username,user_data)
    return success_response(message="更新成功", data=UserInfoResponse.model_validate(user))

@router.put('/password')
async def update_password(
        password_data: UserChangePasswordRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    result = await users.change_password(db, user, password_data.old_password,password_data.new_password)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败，请重试")
    return success_response(message="修改密码成功")









