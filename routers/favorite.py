from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


# 检查新闻收藏装填
@router.get("/check", summary="检查新闻收藏状态")
async def check_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(is_favorite=is_favorited))


# 添加收藏
@router.post("/add", summary="添加收藏")
async def add_favorite(
        data: FavoriteAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)


# 删除收藏
@router.delete("/remove", summary="删除收藏")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")

    return success_response(message="删除收藏成功")


# 获取收藏列表
@router.get("/list", summary="获取收藏列表")
async def get_favorite_list(
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    rows, total = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    }for news, favorite_time, favorite_id in rows ]

    has_more = total > page * page_size
    data = FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more)
    return success_response(message="获取收藏列表成功",data=data)


#清空收藏列表
@router.delete("/clean",summary="清空收藏列表")
async def remove_favorite_list(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    cnt = await favorite.remove_all_favorite(db, user.id)
    return success_response(message=f"清空了{cnt}条记录")












