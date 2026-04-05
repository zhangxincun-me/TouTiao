# TouTiao 头条新闻资讯系统
一个前后端分离的新闻资讯类项目，仿今日头条核心业务场景实现，覆盖用户管理、新闻浏览、分类筛选、内容收藏、浏览历史、热点缓存等完整功能链路。后端基于 Python FastAPI 异步框架开发，前端采用 Vue.js 构建，配套完整的接口规范、数据库设计与架构说明文档，开箱即用，便于二次开发与学习参考。

## ✨ 功能特性
- **用户管理**：用户注册、登录、身份校验与个人信息管理
- **新闻核心**：新闻列表分页查询、分类筛选、详情查看、阅读量统计
- **用户互动**：新闻收藏、个人收藏列表管理、浏览历史自动记录与回溯
- **性能优化**：热点新闻数据缓存模块，降低数据库压力，提升接口响应速度
- **标准化开发**：完整的接口规范文档、后端架构设计文档、数据库初始化脚本
- **前后端分离**：完全解耦的前后端架构，独立部署、灵活扩展、易于维护

## 🛠 技术栈
### 前端
- 核心框架：Vue.js
- 开发语言：JavaScript
- 样式开发：CSS / HTML

### 后端
- 核心框架：FastAPI（Python 异步 Web 框架）
- 开发语言：Python
- ORM 框架：SQLAlchemy
- 数据校验：Pydantic
- 异步驱动：aiomysql
- 缓存模块：自定义热点数据缓存实现

### 数据存储
- 关系型数据库：MySQL 5.7+ / 8.0+
- 缓存扩展：支持 Redis / 本地缓存接入

## 📁 项目目录结构
```
TouTiao/
├── 01-接口规范文档/          # 项目接口规范文档，含所有接口入参、出参、权限说明
├── 02-数据库sql文件/         # 数据库表结构初始化 SQL 脚本
├── 03-前端项目代码/xwzx-news/ # Vue 前端项目完整源码
├── cache/                    # 缓存模块，热点新闻数据的缓存读写逻辑
├── config/                   # 项目配置目录，含数据库连接、缓存参数配置
├── crud/                     # 数据库增删改查操作封装，按业务模块拆分
│   ├── users.py              # 用户相关数据库操作
│   ├── news.py               # 新闻内容相关数据库操作
│   ├── favorite.py           # 新闻收藏相关数据库操作
│   ├── history.py            # 浏览历史相关数据库操作
│   └── news_cache.py         # 缓存数据同步相关操作
├── models/                   # 数据库模型定义，ORM 表结构映射
├── routers/                  # 接口路由模块，所有 API 接口的定义与实现
├── schemas/                  # Pydantic 数据模型，请求/响应参数校验与格式定义
├── utils/                    # 通用工具函数，公共方法封装
├── .gitignore                # Git 忽略文件配置
├── main.py                   # 项目启动入口，FastAPI 应用初始化与服务启动
└── 项目后端设计说明文档.md    # 后端架构设计、模块划分与实现逻辑说明
```

## 🚀 本地运行部署
### 环境准备
- Python 3.8+
- Node.js 14+
- MySQL 5.7+ / 8.0+

### 1. 克隆项目到本地
```bash
git clone https://github.com/zhangxincun-me/TouTiao.git
cd TouTiao
```

### 2. 后端服务启动
1.  创建并激活 Python 虚拟环境
    ```bash
    # 创建虚拟环境
    python -m venv venv

    # Windows 系统激活
    venv\Scripts\activate

    # Mac / Linux 系统激活
    source venv/bin/activate
    ```

2.  安装项目依赖
    ```bash
    pip install fastapi uvicorn sqlalchemy pydantic aiomysql python-multipart
    ```
    若项目根目录有 `requirements.txt`，可直接执行：
    ```bash
    pip install -r requirements_old.txt
    ```

3.  数据库配置
    - 打开 `config/db_config.py`，修改数据库连接信息，配置你的 MySQL 地址、端口、用户名、密码、数据库名
    - 打开 `02-数据库sql文件` 目录，在 MySQL 中执行初始化 SQL 脚本，完成数据库与表结构创建

4.  启动后端服务
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

5.  接口文档访问
    服务启动后，访问 http://127.0.0.1:8000/docs 即可查看 FastAPI 自动生成的交互式接口文档，支持在线调试。

### 3. 前端服务启动
1.  进入前端项目目录
    ```bash
    cd 03-前端项目代码/xwzx-news
    ```

2.  安装前端依赖
    ```bash
    npm install
    ```

3.  启动前端开发服务
    ```bash
    npm run dev
    ```

4.  前端页面访问
    服务启动后，访问 http://127.0.0.1:8080 即可进入项目前端页面。

## 📄 相关文档
- 接口规范：查看 `01-接口规范文档` 目录，获取所有接口的详细定义
- 架构设计：查看 `项目后端设计说明文档.md`，了解后端整体架构与模块设计思路
- 数据库设计：查看 `02-数据库sql文件` 目录，获取表结构设计与初始化脚本

## 👤 作者信息
- GitHub：[@zhangxincun-me](https://github.com/zhangxincun-me)

## 📃 许可证
本项目仅用于学习与交流，未经许可禁止商用。
