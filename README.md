# TouTiao | 头条新闻资讯系统

[](https://fastapi.tiangolo.com/)
[](https://vuejs.org/)
[](https://www.python.org/)

这是一个基于异步架构开发的前后端分离新闻系统。项目深度模拟了“今日头条”的核心业务场景，覆盖了从用户登录、内容分发到高并发缓存的完整链路。

-----

## 🚀 项目亮点

  * **高性能异步后端**：基于 FastAPI + `aiomysql` 实现全链路异步 IO，大幅提升接口并发能力。
  * **现代依赖管理**：推荐使用 Conda 进行环境隔离，规避 Windows 环境下的编译报错。
  * **深度版本兼容**：针对 Python 3.13+ 环境，内置 `bcrypt` 与 `passlib` 兼容性补丁，开箱即用。
  * **多级缓存机制**：支持 Redis 热点数据缓存，具备自动降级策略（Redis 未启动时自动切换至 MySQL）。

-----

## 🛠 技术栈

| 类别 | 技术方案 |
| :--- | :--- |
| **后端框架** | FastAPI (Python 异步) |
| **持久层** | SQLAlchemy 2.0 (Async) + MySQL |
| **缓存** | Redis |
| **安全加密** | Passlib + Bcrypt + JWT (python-jose) |
| **前端框架** | Vue.js + Vite |

-----

## 📁 目录结构

```text
TouTiao/
├── 01-接口规范文档/          # API 详细入参/出参说明
├── 02-数据库sql文件/         # MySQL 表结构初始化脚本
├── 03-前端项目代码/          # Vue 前端完整源码
├── crud/                     # 数据库业务逻辑封装 (DAO 层)
├── models/                   # SQLAlchemy ORM 模型定义
├── routers/                  # API 路由拆分
├── utils/                    # 包含关键的 security 兼容性补丁
├── main.py                   # 项目入口
└── requirements.txt          # 经过验证的依赖清单
```

-----

## ⚙️ 本地快速开始

### 1\. 环境准备 (Conda)

建议使用 Anaconda/Miniconda 管理环境。

```bash
# 创建并激活环境
conda create -n toutiao python=3.13 -y
conda activate toutiao
```

### 2\. 后端部署

1.  **安装依赖**：
    ```bash
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```
2.  **数据库初始化**：
      * 在 MySQL 中执行 `02-数据库sql文件` 下的脚本。
      * 修改 `config/db_config.py` 中的数据库连接字符串。
3.  **启动服务**：
    ```bash
    python main.py
    ```
    访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看交互式文档。

### 3\. 前端部署

```bash
cd 03-前端项目代码/xwzx-news
npm install
npm run dev
```

-----

## ⚠️ 关键技术说明 (必读)

### 关于 Python 3.13 兼容性

由于 `passlib` 库较旧，无法直接适配新版 `bcrypt`。本项目在 `utils/security.py` 中内置了 **Monkey Patch（猴子补丁）**。

  * **自动属性修复**：手动补齐了缺失的 `__about__` 属性。
  * **72 字节截断**：解决了新版 `bcrypt` 对长密码抛出 `ValueError` 的问题。
  * **无需安装编译器**：使用补丁方案后，你无需安装几 GB 的 Visual C++ Build Tools 即可直接运行。

-----

## 📄 许可证

本项目仅供学习与交流使用。

-----
