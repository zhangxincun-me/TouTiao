from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


#数据库的URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app"


#创建异步引擎
async_engine= create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,          #输出SQL日志
    pool_size=10,       #设置连接池中保持连接的持久连接数
    max_overflow=20)    # 设置连接池允许创建的额外连接数

#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,            # 绑定异步引擎
    class_ = AsyncSession,          # 指定类，生产异步引擎的Session
    expire_on_commit = False        # 提交时是否失效,提交后别把内存里的数据删掉
)

#依赖项，获取数据库的会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session         ##返回数据库会话给路由器处理函数
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
