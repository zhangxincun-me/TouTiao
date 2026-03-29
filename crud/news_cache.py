from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cache_categories, get_cached_news_list, set_cache_news_list, \
    get_cached_news_details, set_cache_news_details, set_cache_related_news, get_cached_related_news
from models.news import Category, News
from schemas.base import NewsItemBase


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 先从缓存中查找数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    # 没有再进行数据库查询
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    # 写入缓存
    if categories:
        categories_json = jsonable_encoder(categories)
        await set_cache_categories(categories_json)
    return categories


# 获取指定分类下的新闻列表
async def get_news_list(db: AsyncSession, category_id: int = 0, skip: int = 0, limit: int = 100):
    page = skip // limit + 1
    cached_list = await get_cached_news_list(category_id, page, limit)
    if cached_list:
        return [News(**item) for item in cached_list]

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories_list = result.scalars().all()
    if categories_list:
        news_data = [NewsItemBase.model_validate(item).model_dump(mode='json', by_alias=False) for item in
                     categories_list]
        await set_cache_news_list(category_id, page, limit, news_data)
    return categories_list


# 获取指定分类下的新闻数量
async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只允许一个结果，否则报错


# 获取详细资料
async def get_news_detail(db: AsyncSession, news_id: int):
    news_details = await get_cached_news_details(news_id)
    if news_details:
        return News(**news_details)
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_details = result.scalar_one_or_none()
    if news_details:
        news_dict = jsonable_encoder(news_details)
        await set_cache_news_details(news_dict, news_id)
    return news_details


# 更新浏览量
async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# 查询同类新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    result = await get_cached_related_news(news_id, category_id, limit)
    if result:
        return result

    stmt = select(News).where(News.id != news_id, News.category_id == category_id).order_by(News.views.desc(),
                                                                                           News.publish_time.desc()).limit(
        limit)
    result = await db.execute(stmt)
    related_list = [{
        "id": news_detail.id,
        "title": news_detail.title,
        "image": news_detail.image
    } for news_detail in result.scalars().all()]
    if related_list:
        await set_cache_related_news(related_list, news_id, category_id, limit)
    return related_list
