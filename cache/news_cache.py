from typing import List, Dict, Any, Optional
from config.cache_conf import set_cache, get_cache, get_json_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX ="newsList:"
NEWS_DETAILS = "news:details:"
RELATED_NEWS = "news:related:"

# 获取新闻分类缓存
# 读取
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)


# 写入缓存
# 分类，配置 7200  列表：600 详情： 1800 验证码： 120
async def set_cache_categories(data : List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)


# 缓存新闻列表list

# 写入缓存
async def set_cache_news_list(category_id: Optional[int], page: int, size: int, news_list: List[Dict[str, Any]],expire: int = 7200):
    category_part = category_id if category_id is not None else "news_all"
    key = f'{NEWS_LIST_PREFIX}{category_part}:{page}:{size}'
    return await set_cache(key, news_list, expire)

# 读取
async def get_cached_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "news_all"
    key = f'{NEWS_LIST_PREFIX}{category_part}:{page}:{size}'
    return await get_json_cache(key)


# 获取新闻详情

#写入
async def set_cache_news_details(data: Dict[str, Any], news_id: int, expire: int = 7200):
    key = f'{NEWS_DETAILS}{news_id}'
    return await set_cache(key, data, expire)

# 读取
async def get_cached_news_details(news_id: int):
    key = f'{NEWS_DETAILS}{news_id}'
    return await get_json_cache(key)

# 查询同类型新闻

# 写入
async def set_cache_related_news(data: List[Dict[str, Any]], news_id: int, category_id: int, limit: int = 5, expire: int = 3600):
    category_part = category_id if category_id is not None else "news_all"
    key = f'{RELATED_NEWS}:{category_part}:{news_id}:{limit}'
    return await set_cache(key, data, expire)


# 读取
async def get_cached_related_news(news_id: int, category_id: int, limit: int = 5):
    category_part = category_id if category_id is not None else "news_all"
    key = f'{RELATED_NEWS}:{category_part}:{news_id}:{limit}'
    return await get_json_cache(key)






