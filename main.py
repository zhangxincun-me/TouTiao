import uvicorn
from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #允许的源 开发阶段允许所有的源，生产环境需要指定源
    allow_credentials=True, #允许携带cookie
    allow_methods=["*"],  #允许的请求方法
    allow_headers=["*"]  #允许请求头
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

#挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
