import json
from typing import Any
import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

#创建链接客户端
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True #是否解码为字符串
)

#设置和读取
#读取字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败:{e}")
        return None

#读取list 和dict
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取JSON 缓存失败：{e}")
        return None

#设置缓存 key value expire
async def set_cache(key:str, value:Any, expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            value = json.dumps(value,ensure_ascii=False)
        await redis_client.setex(key, expire,value)
        return True
    except Exception as e:
        print('设置缓存失败: {e}')
        return False






























































