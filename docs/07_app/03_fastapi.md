# 

### 为什么 FastAPI 突然流行？

1. **性能优势**
   - 基于 **ASGI**（异步服务器网关接口），比传统的 **WSGI**（如 Flask、Django）更高效，适合高并发场景（如微服务、实时 API）。
   - 底层依赖 **Starlette**（高性能异步框架）和 **Pydantic**（数据验证库），速度接近 **Node.js** 和 **Go**。
2. **开发者友好**
   - **自动生成 API 文档**（集成 Swagger UI 和 ReDoc），减少手动维护文档的工作量。
   - **类型提示（Type Hints）**：结合 Python 3.6+ 的类型系统，提升代码可读性和可维护性。
3. **现代技术栈适配**
   - 天然支持 **RESTful API**、**GraphQL**、**WebSocket**，适合云原生和微服务架构。
   - 与 **Docker**、**Kubernetes**、**Serverless** 等云技术无缝集成。
4. **行业需求变化**
   - 企业对高性能、低延迟的 API 需求增加（如 AI 服务、大数据接口）。
   - 初创公司和互联网企业倾向于轻量级框架，降低开发和运维成本。


> 以前大家用 Flask，够轻量但类型检查不友好，Django 太重了；FastAPI 成了中间地带的最优解。



### 基本特性

#### **1. 核心概念**
- **路由与请求处理**：如何定义路由（`@app.get/post`）、处理路径参数和查询参数。
- **依赖注入（Dependency Injection）**：FastAPI 的依赖系统（如 `Depends`）如何管理代码复用（如数据库会话、权限验证）。
- **Pydantic 模型**：数据验证、序列化（如请求/响应模型的嵌套结构）。
- **异步支持（Async/Await）**：如何编写异步视图函数，与数据库（如 SQLAlchemy 2.0+、Tortoise-ORM）或其他服务（如 HTTP 请求）交互。

#### **2. 数据库集成**
- **SQL 数据库**：搭配 **SQLAlchemy**（同步或异步模式）或 **Tortoise-ORM**（异步 ORM）。
- **NoSQL 数据库**：如 **MongoDB**（通过 Motor 异步驱动）、**Redis**（缓存或消息队列）。
- **数据库迁移工具**：如 **Alembic**（需结合 SQLAlchemy）。

#### **3. 高级特性**
- **中间件（Middleware）**：如何添加全局逻辑（如日志、CORS 处理）。
- **WebSocket 实时通信**：与前端建立双向通信。
- **后台任务（Background Tasks）**：处理耗时操作（如发送邮件）而不阻塞主线程。
- **测试与部署**：
  - 测试：使用 `TestClient` 编写单元测试。
  - 部署：通过 **Uvicorn** 或 **Gunicorn** 运行，配合 **Nginx** 反向代理。

#### **4. 安全相关**
- **OAuth2 与 JWT**：实现用户认证（如 `fastapi.security` 模块）。
- **CORS**：处理跨域请求。
- **敏感数据保护**：环境变量管理（如 `pydantic-settings`）。