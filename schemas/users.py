from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str
    password: str


class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=500, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


# userinfo 对应的类：基础类+info类（id,用户名）
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 对象中取值
    )


# data数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容
        from_attributes=True  # 允许从 ORM 对象中取值
    )

class UserUpdateRequest(BaseModel):
    nickname: str =None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None
