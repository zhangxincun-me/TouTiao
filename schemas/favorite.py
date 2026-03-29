from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase

#检查新闻收藏状态响应参数
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # 关键！允许用字段名赋值
    )

#添加收藏请求参数
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


# 规划两个类：一个是新闻模型类 + 收藏的模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

#收藏列表接口响应模型
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )










