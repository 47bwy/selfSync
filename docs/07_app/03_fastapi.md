# 

⚠️ [官方教程](https://fastapi.tiangolo.com/zh/tutorial/)

### 🔍 为什么 FastAPI 突然流行？

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



### 🧩 基本特性

**1. 核心概念**
- **路由与请求处理**：如何定义路由（`@app.get/post`）、处理路径参数和查询参数。

- **依赖注入（Dependency Injection）**：FastAPI 的依赖系统（如 `Depends`）如何管理代码复用（如数据库会话、权限验证）。

- **Pydantic 模型**：数据验证、序列化（如请求/响应模型的嵌套结构）。

- **异步支持（Async/Await）**：如何编写异步视图函数，与数据库（如 SQLAlchemy 2.0+、Tortoise-ORM）或其他服务（如 HTTP 请求）交互。

**2. 数据库集成**
- **SQL 数据库**：搭配 **SQLAlchemy**（同步或异步模式）或 **Tortoise-ORM**（异步 ORM）。

- **NoSQL 数据库**：如 **MongoDB**（通过 Motor 异步驱动）、**Redis**（缓存或消息队列）。

- **数据库迁移工具**：如 **Alembic**（需结合 SQLAlchemy）。

**3. 高级特性**
- **中间件（Middleware）**：如何添加全局逻辑（如日志、CORS 处理）。

- **WebSocket 实时通信**：与前端建立双向通信。

- **后台任务（Background Tasks）**：处理耗时操作（如发送邮件）而不阻塞主线程。

- **测试与部署**：
  - 测试：使用 `TestClient` 编写单元测试。

  - 部署：通过 **Uvicorn** 或 **Gunicorn** 运行，配合 **Nginx** 反向代理。

**4. 安全相关**
- **OAuth2 与 JWT**：实现用户认证（如 `fastapi.security` 模块）。

- **CORS**：处理跨域请求。

- **敏感数据保护**：环境变量管理（如 `pydantic-settings`）。



### 📚 学习内容

#### 🎯 路径参数（Path Parameters）：

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

| 功能               | 作用                                                         |
| ------------------ | ------------------------------------------------------------ |
| 声明路径参数的类型 | 使用 Python 标准类型注解，声明路径操作函数中路径参数的类型   |
| 数据转换           | **FastAPI** 通过类型声明自动**解析**请求中的数据             |
| 数据校验           | **FastAPI** 使用 Python 类型声明实现了数据校验               |
| 查看文档           | .../docs 自动生成的 API 文档                                 |
| 备选文档           | .../redoc 生成的备选 API 文档                                |
| Pydantic           | FastAPI 充分地利用了 [Pydantic](https://docs.pydantic.dev/) 的优势，用它在后台校验数据。 |
| 顺序很重要         | *路径操作*是按顺序依次运行的                                 |
| 预设值             | 接收预设的*路径参数*                                         |

#### 🎯 查询参数（Query Parameters）：

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
# needy 为必选参数
```

声明的参数不是路径参数时，路径操作函数会把该参数自动解释为**查询**参数。

| 功能               | 作用                                                     |
| ------------------ | -------------------------------------------------------- |
| 默认值             | 查询参数不是路径的固定内容，它是可选的，还支持默认值     |
| 可选参数           | 把默认值设为 `None` 即可声明**可选的**查询参数           |
| 查询参数类型转换   | 参数还可以声明为 `bool` 类型，FastAPI 会自动转换参数类型 |
| 多个路径和查询参数 | **FastAPI** 可以识别同时声明的多个路径参数和查询参数     |
| 必选查询参数       | 如果要把查询参数设置为**必选**，就不要声明默认值         |


#### 🎯 请求体（Request Body）：

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

FastAPI 使用请求体从客户端（例如浏览器）向 API 发送数据。

请求体是客户端发送给 API 的数据。响应体是 API 发送给客户端的数据。

API 基本上肯定要发送响应体，但是客户端不一定发送请求体。


| 功能               | 作用                                                     |
| ------------------ | -------------------------------------------------------- |
| Pydantic             | 导入 Pydantic 的 BaseModel     |
| 创建数据模型 | 把数据模型声明为继承 `BaseModel` 的类 |
| 声明请求体参数 | 使用与声明路径和查询参数相同的方式声明请求体，把请求体添加至*路径操作* |
| API 文档 | Pydantic 模型的 JSON 概图是 OpenAPI 生成的概图部件，可在 API 文档中显示 |
| 编辑器支持 | 在编辑器中，函数内部均可使用类型提示、代码补全（如果接收的不是 Pydantic 模型，而是**字典**，就没有这样的支持） |
| 使用模型 | 在*路径操作*函数内部直接访问模型对象的属性 |
| 请求体 + 路径参数 | **FastAPI** 支持同时声明路径参数和请求体 |
| 请求体 + 路径参数 + 查询参数 | **FastAPI** 支持同时声明**请求体**、**路径参数**和**查询参数**。**FastAPI** 能够正确识别这三种参数，并从正确的位置获取数据。 |



⚠️ 仅使用 Python 类型声明，**FastAPI** 就可以：

- 以 JSON 形式读取请求体
- （在必要时）把请求体转换为对应的类型
- 校验数据：
  - 数据无效时返回错误信息，并指出错误数据的确切位置和内容
- 把接收的数据赋值给参数`item`
  - 把函数中请求体参数的类型声明为 `Item`，还能获得代码补全等编辑器支持
- 为模型生成 [JSON Schema](https://json-schema.org/)，在项目中所需的位置使用
- 这些概图是 OpenAPI 概图的部件，用于 API 文档 UI



⚠️ 函数参数按如下规则进行识别：

- **路径**中声明了相同参数的参数，是路径参数

- 类型是（`int`、`float`、`str`、`bool` 等）**单类型**的参数，是**查询**参数

- 类型是 **Pydantic 模型**的参数，是**请求体**

  

⚠️ 通过简短、直观的 Python 标准类型声明，**FastAPI** 可以获得：

- 编辑器支持：错误检查，代码自动补全等
- 数据**解析**
- 数据校验
- API 注解和 API 文档

只需要声明一次即可。

这可能是除了性能以外，**FastAPI** 与其它框架相比的主要优势。


#### 🎯 查询参数和字符串校验

**FastAPI** 允许为参数声明额外的信息和校验。

```py
from typing import Union

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

| 功能               | 作用                                                     |
| :----------------- | -------------------------------------------------------- |
| 额外的校验        | 我们打算添加约束条件：即使 `q` 是可选的，但只要提供了该参数，则该参数值**不能超过50个字符的长度**。 |
| 使用 `Query` 作为默认值 | 将 `Query` 用作查询参数的默认值 |
| 添加更多校验 | 还可以添加 `min_length` 参数 |
| 添加正则表达式 | 可以定义一个参数值必须匹配的正则表达式 |
| 默认值 | 可以向 `Query` 的第一个参数传入 `None` 用作查询参数的默认值，以同样的方式也可以传递其他默认值。 |
| 声明为必需参数 | 不需要声明额外的校验或元数据时，只需不声明默认值就可以使 `q` 参数成为必需参数 |
| 使用`None`声明必需参数 | 可以声明一个参数可以接收`None`值，但它仍然是必需的。这将强制客户端发送一个值，即使该值是`None`。 |
| 查询参数列表 / 多个值 | 使用 `Query` 显式地定义查询参数时，还可以声明它去接收一组值，或换句话来说，接收多个值。 |
| 具有默认值的查询参数列表 / 多个值 | 可以定义在没有任何给定值时的默认 `list` 值 |
| 声明更多元数据 | 可以添加 `title`以及 `description` |
| 别名参数 | 可以用 `alias` 参数声明一个别名，该别名将用于在 URL 中查找查询参数值 |
| 弃用参数 | 将参数 `deprecated=True` 传入 `Query` |

⚠️ 通用的校验和元数据：

- `alias`
- `title`
- `description`
- `deprecated`

⚠️ 特定于字符串的校验：

- `min_length`
- `max_length`
- `regex`


#### 🎯 路径参数和数值校验

与使用 `Query` 为查询参数声明更多的校验和元数据的方式相同，也可以使用 `Path` 为路径参数声明相同类型的校验和元数据。

```python
from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

| 功能               | 作用                                                     |
| :----------------- | -------------------------------------------------------- |
| 声明元数据                   | 声明路径参数 `item_id`的 `title` 元数据值 |
| 按需对参数排序 | 对 **FastAPI** 来说这无关紧要。它将通过参数的名称、类型和默认值声明（`Query`、`Path` 等）来检测参数，而不在乎参数的顺序。 |
| 按需对参数排序的技巧 | 传递 `*` 作为函数的第一个参数。Python 不会对该 `*` 做任何事情，但是它将知道之后的所有参数都应作为关键字参数（键值对），也被称为 `kwargs`，来调用。 |
| 数值校验：大于等于 | 使用 `Query` 和 `Path`可以声明字符串约束，但也可以声明数值约束。 |
| 数值校验：大于和小于等于 | 同样的规则适用于`gt`  `le` |
| 数值校验：浮点数、大于和小于 | 数值校验同样适用于 `float` 值。 |


⚠️ 与 **查询参数和字符串校验** 相同的方式使用 `Query`、`Path`（以及其他还没见过的类）声明元数据和字符串校验。

而且还可以声明数值校验：

- `gt`：大于（`g`reater `t`han）
- `ge`：大于等于（`g`reater than or `e`qual）
- `lt`：小于（`l`ess `t`han）
- `le`：小于等于（`l`ess than or `e`qual）


#### 🎯 查询参数模型

如果有一组具有相关性的**查询参数**，可以创建一个 **Pydantic 模型**来声明它们。

这将允许在**多个地方**去**复用模型**，并且一次性为所有参数声明验证和元数据。

```python
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

| 功能                         | 作用                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| 使用 Pydantic 模型的查询参数 | 在一个 **Pydantic 模型**中声明需要的**查询参数**，然后将参数声明为 `Query` |
| 禁止额外的查询参数           | 可以使用 Pydantic 的模型配置来 `forbid` 任何 `extra` 字段    |

⚠️ 总结：

- **`Annotated`** 主要用来为类型提供元数据，适合需要附加约束或描述的场景，FastAPI 中常用来描述请求参数的额外信息。
- **`Union`** 允许指定一个值可能是多种类型中的任何一种，适用于参数或返回值可能是不同类型的情况，FastAPI 用它来支持多种类型的参数验证。

 

#### 🎯 请求体 - 多个参数

```python
from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
  
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
  
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

| 功能                                  | 作用                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| 混合使用 `Path`、`Query` 和请求体参数 | 可以随意地混合使用 `Path`、`Query` 和请求体参数声明，**FastAPI** 会知道该如何处理。 |
| 多个请求体参数                        | 可以声明多个请求体参数，例如 `item` 和 `user`<br />在这种情况下，**FastAPI** 将注意到该函数中有多个请求体参数（两个 Pydantic 模型参数）<br />因此，它将使用参数名称作为请求体中的键（字段名称） |
| 请求体中的单一值                      | 可以使用 `Body` 指示 **FastAPI** 将其作为请求体的另一个键进行处理 |
| 多个请求体参数和查询参数              | 除了请求体参数外，还可以在任何需要的时候声明额外的查询参数<br />由于默认情况下单一值被解释为查询参数，因此不必显式地添加 `Query` |
| 嵌入单个请求体参数                    | 它期望一个拥有 `item` 键并在值中包含模型内容的 JSON，就像在声明额外的请求体参数时所做的那样<br />可以使用一个特殊的 `Body` 参数 `embed` |



#### 🎯 请求体 - 字段

与在*路径操作函数*中使用 `Query`、`Path` 、`Body` 声明校验与元数据的方式一样，可以使用 Pydantic 的 `Field` 在 Pydantic 模型内部声明校验和元数据。

```python
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

实际上，`Query`、`Path` 都是 `Params` 的子类，而 `Params` 类又是 Pydantic 中 `FieldInfo` 的子类。

Pydantic 的 `Field` 返回也是 `FieldInfo` 的类实例。

`Body` 直接返回的也是 `FieldInfo` 的子类的对象。后文还会介绍一些 `Body` 的子类。

注意，从 `fastapi` 导入的 `Query`、`Path` 等对象实际上都是返回特殊类的函数。



#### 🎯 请求体 - 嵌套模型

使用 **FastAPI**，可以定义、校验、记录文档并使用任意深度嵌套的模型（归功于Pydantic）。

```python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
```

| 功能                     | 作用                                                         |
| ------------------------ | ------------------------------------------------------------ |
| List 字段                | 可以将一个属性定义为拥有子元素的类型。例如 Python `list`     |
| 具有子类型的 List 字段   | 使用方括号 `[` 和 `]` 将子类型作为「类型参数」传入，比如：`List[str]` |
| Set 类型                 | 比如：`set[str]`                                             |
| 嵌套模型                 | Pydantic 模型的每个属性都具有类型，但是这个类型本身可以是另一个 Pydantic 模型 |
| 特殊的类型和校验         | 在 `Image` 模型中我们有一个 `url` 字段，我们可以把它声明为 Pydantic 的 `HttpUrl`，而不是 `str` |
| 带有一组子模型的属性     | 可以将 Pydantic 模型用作 `list`、`set` 等的子类型，比如：`list[Image]` |
| 深度嵌套模型             | 可以定义任意深度的嵌套模型，比如：`Offer`                    |
| 纯列表请求体             | 期望的 JSON 请求体的最外层是一个 JSON `array`（即 Python `list`），则可以在路径操作函数的参数中声明此类型 |
| 任意 `dict` 构成的请求体 | 可以将请求体声明为使用某类型的键和其他类型值的 `dict`，比如：`dict[int, float]` |



#### 🎯 模式的额外信息 - 例子

可以在JSON模式中定义额外的信息。一个常见的用例是添加一个将在文档中显示的`example`。

```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
    
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

| 功能                    | 作用                                                         |
| ----------------------- | ------------------------------------------------------------ |
| Pydantic `schema_extra` | 可以使用 `Config` 和 `schema_extra` 为Pydantic模型声明一个示例 |
| `Field` 的附加参数      | 在 `Field`, `Path`, `Query`, `Body` 和其他之后将会看到的工厂函数，可以为JSON 模式声明额外信息，<br />也可以通过给工厂函数传递其他的任意参数来给JSON 模式声明额外信息 |
| `Body` 额外参数         | 以通过传递额外信息给 `Field` 同样的方式操作`Path`, `Query`, `Body`等 |



#### 🎯 额外数据类型

到目前为止，您一直在使用常见的数据类型，如:

- `int`
- `float`
- `str`
- `bool`

但是您也可以使用更复杂的数据类型。

您仍然会拥有现在已经看到的相同的特性:

- 很棒的编辑器支持。
- 传入请求的数据转换。
- 响应数据转换。
- 数据验证。
- 自动补全和文档。

```python
from datetime import datetime, time, timedelta
from typing import Annotated, Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[Union[time, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

| 功能               | 作用                                                         |
| ------------------ | ------------------------------------------------------------ |
| UUID               | 一种标准的 "通用唯一标识符" ，在许多数据库和系统中用作ID。   |
| datetime.datetime  | 一个 Python `datetime.datetime`                              |
| datetime.date      | Python `datetime.date`                                       |
| datetime.time      | 一个 Python `datetime.time`                                  |
| datetime.timedelta | 一个 Python `datetime.timedelta`,，在请求和响应中将表示为 `float` 代表总秒数 |
| frozenset          | 在请求和响应中，作为 `set` 对待                              |
| bytes              | 标准的 Python `bytes`                                        |
| Decimal            | 标准的 Python `Decimal`                                      |



#### 🎯 Cookie 参数

```python
from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
  
  
class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```



#### 🎯 Header 参数

```python
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
  
class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```



#### 🎯 响应模型

可以控制 response 中的内容，根据需求展示。将输出数据限制在该模型定义内。

可以在任意的*路径操作*中使用 `response_model` 参数来声明用于响应的模型：

- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.delete()`
- 等等。

```python
from typing import Any, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
```

⚠️ 注意，`response_model`是「装饰器」方法（`get`，`post` 等）的一个参数。不像之前的所有参数和请求体，它不属于*路径操作函数*。



它接收的类型与将为 Pydantic 模型属性所声明的类型相同，因此它可以是一个 Pydantic 模型，但也可以是一个由 Pydantic 模型组成的 `list`，例如 `List[Item]`。

FastAPI 将使用此 `response_model` 来：

- 将输出数据转换为其声明的类型。
- 校验数据。
- 在 OpenAPI 的*路径操作*中为响应添加一个 JSON Schema。
- 并在自动生成文档系统中使用。

| 功能                 | 作用                                                         |
| -------------------- | ------------------------------------------------------------ |
| 返回与输入相同的数据 | 正在使用此模型声明输入数据，并使用同一模型声明输出数据       |
| 添加输出模型         | 可以创建一个有明文密码的输入模型和一个没有明文密码的输出模型 |
| 响应模型编码参数     | 响应模型可以具有默认值，也可以从结果中忽略它们的默认值       |
|                      | 默认值字段有实际值的数据                                     |
|                      | 具有与默认值相同值的数据                                     |



#### 🎯 更多模型

下面的代码展示了不同模型处理密码字段的方式，及使用位置的大致思路：

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


# **user_in.model_dump()
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

| 功能                   | 作用                                                         |
| ---------------------- | ------------------------------------------------------------ |
| 减少重复               | 上面的这些模型共享了大量数据，拥有重复的属性名和类型。       |
| `Union` 或者 `anyOf`   | 定义 `Union`类型时，要把详细的类型写在前面，然后是不太详细的类型。 |
| 模型列表               | 使用同样的方式也可以声明由对象列表构成的响应。               |
| 任意 `dict` 构成的响应 | 意的 `dict` 都能用于声明响应，只要声明键和值的类型，无需使用 Pydantic 模型。 |



#### 🎯 响应状态码

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
  
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

与 `response_model`  一样，`status_code` 是（`get`、`post` 等）**装饰器**方法中的参数。与之前的参数和请求体不同，不是*路径操作函数*的参数。



#### 🎯 表单数据和表单模型

```python
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

⚠️ 声明表单体要显式使用 `Form` ，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数。

⚠️ 可在一个*路径操作*中声明多个 `Form` 参数，但不能同时声明要接收 JSON 的 `Body` 字段。因为此时请求体的编码是 `application/x-www-form-urlencoded`，不是 `application/json`。

```python
from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

⚠️ 可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段



#### 🎯 请求文件

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

⚠️ 声明文件体必须使用 `File`，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数。



`UploadFile` 与 `bytes` 相比有更多优势：

- 使用`spooled`文件：

  - 存储在内存的文件超出最大上限时，FastAPI 会把文件存入磁盘；

- 这种方式更适于处理图像、视频、二进制文件等大型文件，好处是不会占用所有内存；

- 可获取上传文件的元数据；

- 自带 [file-like](https://docs.python.org/zh-cn/3/glossary.html#term-file-like-object) `async` 接口；

- 暴露的 Python [`SpooledTemporaryFile`](https://docs.python.org/zh-cn/3/library/tempfile.html#tempfile.SpooledTemporaryFile) 对象，可直接传递给其他预期「file-like」对象的库。



🧩 `UploadFile` 的属性如下：

- `filename`：上传文件名字符串（`str`），例如， `myimage.jpg`；
- `content_type`：内容类型（MIME 类型 / 媒体类型）字符串（`str`），例如，`image/jpeg`；
- `file`： `SpooledTemporaryFile` file-like 对象。其实就是 Python文件，可直接传递给其他预期 `file-like` 对象的函数或支持库。

🧩 `UploadFile` 支持以下 `async` 方法，（使用内部 `SpooledTemporaryFile`）可调用相应的文件方法。

- `write(data)`：把 `data` （`str` 或 `bytes`）写入文件；

- `read(size)`：按指定数量的字节或字符（`size` (`int`)）读取文件内容；

- `seek(offset)`：移动至文件 `offset` `（int）`字节处的位置；

  - 例如，`await myfile.seek(0)` 移动到文件开头；

  - 执行 `await myfile.read()` 后，需再次读取已读取内容时，这种方法特别好用；

- `close()`：关闭文件。

因为上述方法都是 `async` 方法，要搭配「await」使用。

| 功能                          | 作用                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| 可选文件上传                  | 可以通过使用标准类型注解并将 None 作为默认值的方式将一个文件参数设为可选 |
| 带有额外元数据的 `UploadFile` | 可以将 `File()` 与 `UploadFile` 一起使用，例如，设置额外的元数据，description="" |
| 多文件上传                    | 可用同一个「表单字段」发送含多个文件的「表单数据」。上传多个文件时，要声明含 `bytes` 或 `UploadFile` 的列表（`List`） |
| 带有额外元数据的多文件上传    | 可以为 `File()` 设置额外参数, 即使是 `UploadFile`            |



#### 🎯请求表单与文件

```python
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```



#### 🎯 处理错误

🧩 使用 `HTTPException`  

`HTTPException` 是额外包含了和 API 有关数据的常规 Python 异常。因为是 Python 异常，所以不能 `return`，只能 `raise`。

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

触发 `HTTPException` 时，可以用参数 `detail` 传递任何能转换为 JSON 的值，不仅限于 `str`。

还支持传递 `dict`、`list` 等数据结构。

**FastAPI** 能自动处理这些数据，并将之转换为 JSON。

🧩 添加自定义响应头

有些场景下要为 HTTP 错误添加自定义响应头。例如，出于某些方面的安全需要。

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
```

🧩 安装自定义异常处理器

添加自定义处理器，要使用 **Starlette 的异常工具**。

🧩 覆盖默认异常处理器

**FastAPI** 自带了一些默认异常处理器。不过，也可以使用自定义处理器覆盖默认异常处理器。

| 功能                                   | 作用                                                         |
| -------------------------------------- | ------------------------------------------------------------ |
| 覆盖请求验证异常                       | 请求中包含无效数据时（类型错误等），**FastAPI** 内部会触发 `RequestValidationError`。 |
| 覆盖 `HTTPException` 错误处理器        | 只为错误返回纯文本响应，而不是返回 JSON 格式的内容           |
| 使用 `RequestValidationError` 的请求体 | 开发时，可以用这个请求体生成日志、调试错误，并返回给用户。包含其接收到的无效数据请求的 `body` |
| 复用 **FastAPI** 异常处理器            | FastAPI 支持先对异常进行某些处理，然后再使用 **FastAPI** 中处理该异常的默认异常处理器。<br />从 `fastapi.exception_handlers` 中导入要复用的默认异常处理器 |

⚠️

```
FastAPI HTTPException vs Starlette HTTPException¶
FastAPI 也提供了自有的 HTTPException。

FastAPI 的 HTTPException 继承自 Starlette 的 HTTPException 错误类。

它们之间的唯一区别是，FastAPI 的 HTTPException 可以在响应中添加响应头。

OAuth 2.0 等安全工具需要在内部调用这些响应头。

因此可以继续像平常一样在代码中触发 FastAPI 的 HTTPException 。

但注册异常处理器时，应该注册到来自 Starlette 的 HTTPException。

这样做是为了，当 Starlette 的内部代码、扩展或插件触发 Starlette HTTPException 时，处理程序能够捕获、并处理此异常。
```





#### 🎯 路径操作配置

*路径操作装饰器*支持多种配置参数。

通过传递参数给*路径操作装饰器* ，即可轻松地配置*路径操作*、添加元数据。

```python
from typing import Set, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()

    
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

| 功能                            | 作用                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| `status_code` 状态码            | `status_code` 用于定义*路径操作*响应中的 HTTP 状态码。可以直接传递 `int` 代码， 比如 `404`。 |
| `tags` 参数                     | `tags` 参数的值是由 `str` 组成的 `list` （一般只有一个 `str` ），`tags` 用于为*路径操作*添加标签 |
| `summary` 和 `description` 参数 |                                                              |
| 文档字符串（`docstring`）       | 描述内容比较长且占用多行时，可以在函数的 docstring 中声明*路径操作*的描述 |
| 响应描述                        | `esponse_description` 参数用于定义响应的描述说明             |
| 弃用*路径操作*                  | `deprecated` 参数可以把*路径操作*标记为弃用，无需直接删除    |



#### 🎯 JSON 兼容编码器

在某些情况下，可能需要将数据类型（如Pydantic模型）转换为与JSON兼容的数据类型（如`dict`、`list`等）。

使用`jsonable_encoder`，它接收一个对象，比如Pydantic模型，并会返回一个JSON兼容的版本。

它将Pydantic模型转换为`dict`，并将`datetime`转换为`str`。

调用它的结果后就可以使用Python标准编码中的`json.dumps()`



#### 🎯 请求体 - 更新数据

| 功能                    | 作用                                   |
| ----------------------- | -------------------------------------- |
| 用 `PUT` 更新数据       | `PUT` 用于接收替换现有数据的数据。     |
| 用 `PATCH` 进行部分更新 | 只发送要更新的数据，其余数据保持不变。 |

简而言之，更新部分数据应：

- 使用 `PATCH` 而不是 `PUT` （可选，也可以用 `PUT`）；

- 提取存储的数据；

- 把数据放入 Pydantic 模型；

- 生成不含输入模型默认值的 `dict`（使用`exclude_unset`参数）；

  - 只更新用户设置过的值，不用模型中的默认值覆盖已存储过的值。

- 为已存储的模型创建副本，用接收的数据更新其属性 （使用 `update` 参数）。

- 把模型副本转换为可存入数据库的形式（比如，使用`jsonable_encoder`）。

  - 这种方式与 Pydantic 模型的 `.dict()` 方法类似，但能确保把值转换为适配 JSON 的数据类型，例如， 把 `datetime` 转换为 `str` 。

- 把数据保存至数据库；

- 返回更新后的模型。



#### 🎯 依赖项

编程中的**「依赖注入」**是声明代码（本文中为*路径操作函数* ）运行所需的，或要使用的「依赖」的一种方式。

依赖注入常用于以下场景：

- 共享业务逻辑（复用相同的代码逻辑）
- 共享数据库连接
- 实现安全、验证、角色权限
- 等……

上述场景均可以使用**依赖注入**，将代码重复最小化。



虽然，在路径操作函数的参数中使用 `Depends` 的方式与 `Body`、`Query` 相同，但 `Depends` 的工作方式略有不同。

这里只能传给 Depends 一个参数。

且该参数必须是可调用对象，比如函数。

该函数接收的参数和*路径操作函数*的参数一样。



其他与「依赖注入」概念相同的术语为：

- 资源（Resource）
- 提供方（Provider）
- 服务（Service）
- 可注入（Injectable）
- 组件（Component）



🧩 类作为依赖项

类是可调用的。

init 参数指定数据类型，也就是提供元数据。



🧩 子依赖项

FastAPI 支持创建含**子依赖项**的依赖项。

并且，可以按需声明任意**深度**的子依赖项嵌套层级。

**FastAPI** 负责处理解析不同深度的子依赖项。



如果在同一个*路径操作* 多次声明了同一个依赖项，例如，多个依赖项共用一个子依赖项，**FastAPI** 在处理同一请求时，只调用一次该子依赖项。

FastAPI 不会为同一个请求多次调用同一个依赖项，而是把依赖项的返回值进行「缓存」，并把它传递给同一请求中所有需要使用该返回值的「依赖项」。



🧩 路径操作装饰器依赖项

路径操作装饰器依赖项（简称为**“路径装饰器依赖项”**）的执行或解析方式和普通依赖项一样，但就算这些依赖项会返回值，它们的值也不会传递给*路径操作函数*。



🧩 全局依赖项

通过与定义**路径装饰器依赖项**类似的方式，可以把依赖项添加至整个 `FastAPI` 应用。

这样一来，就可以为所有*路径操作*应用该依赖项。

app = FastAPI(dependencies=[Depends(...), Depends(...)])



🧩 使用yield的依赖项

FastAPI支持在完成后执行一些额外步骤的依赖项.

为此，需要使用 `yield` 而不是 `return`，然后再编写这些额外的步骤（代码）。



⚠️ 确保在每个依赖中只使用一次 `yield`。

⚠️ 在包含 `yield` 和 `except` 的依赖项中一定要 `raise`



#### 🎯 安全性

| 名称                           | 解释                                                         |
| ------------------------------ | ------------------------------------------------------------ |
| OAuth2                         | OAuth2是一个规范，它定义了几种处理身份认证和授权的方法。<br />它是一个相当广泛的规范，涵盖了一些复杂的使用场景。<br />它包括了使用「第三方」进行身份认证的方法。<br />这就是所有带有「使用 Facebook，Google，Twitter，GitHub 登录」的系统背后所使用的机制。 |
| OAuth 1                        | 有一个 OAuth 1，它与 OAuth2 完全不同，并且更为复杂，因为它直接包含了有关如何加密通信的规范。<br />如今它已经不是很流行，没有被广泛使用了。 |
| OpenID Connect                 | OpenID Connect 是另一个基于 **OAuth2** 的规范。<br />它只是扩展了 OAuth2，并明确了一些在 OAuth2 中相对模糊的内容，以尝试使其更具互操作性。 |
| OpenID（非「OpenID Connect」） | 还有一个「OpenID」规范。它试图解决与 **OpenID Connect** 相同的问题，但它不是基于 OAuth2。<br />如今它已经不是很流行，没有被广泛使用了。 |



🧩 OpenAPI

OpenAPI（以前称为 Swagger）是用于构建 API 的开放规范（现已成为 Linux Foundation 的一部分）。

⚠️ **FastAPI** 基于 **OpenAPI**。

这就是使多个自动交互式文档界面，代码生成等成为可能的原因。

OpenAPI 有一种定义多个安全「方案」的方法。

通过使用它们，可以利用所有这些基于标准的工具，包括这些交互式文档系统。

OpenAPI 定义了以下安全方案：

- `apiKey`：一个特定于应用程序的密钥，可以来自：

  - 查询参数。
  - 请求头。
  - cookie。

- `http`：标准的 HTTP 身份认证系统，包括：

  - `bearer`: 一个值为 `Bearer` 加令牌字符串的 `Authorization` 请求头。这是从 OAuth2 继承的。
  - HTTP Basic 认证方式。
  - HTTP Digest，等等。

- `oauth2`：所有的 OAuth2 处理安全性的方式（称为「流程」）。 
以下几种流程适合构建 OAuth 2.0 身份认证的提供者（例如 Google，Facebook，Twitter，GitHub 等）：`implicit` `clientCredentials` `authorizationCode`

  - 但是有一个特定的「流程」可以完美地用于直接在同一应用程序中处理身份认证：
    - `password`：接下来的几章将介绍它的示例。

- `openIdConnect`：提供了一种定义如何自动发现 OAuth2 身份认证数据的方法。

  - 此自动发现机制是 OpenID Connect 规范中定义的内容。



| 功能                                      | 解释                                                         |
| ----------------------------------------- | ------------------------------------------------------------ |
| 获取当前用户                              | @app.get("/users/me") <br />async def read_users_me(current_user: User = Depends(get_current_user)):<br /<br />return current_user |
| OAuth2 实现简单的 Password 和 Bearer 验证 | OAuth2 规范要求使用**密码流**时，客户端或用户必须以表单数据形式发送 `username` 和 `password` 字段。<br />async def login(form_data: OAuth2PasswordRequestForm = Depends()): |
| OAuth2 实现密码哈希与 Bearer JWT 令牌验证 | JWT 即**JSON 网络令牌**（JSON Web Tokens）。是一种将 JSON 对象编码为没有空格，且难以理解的长字符串的标准。<br />**哈希**是指把特定内容（本例中为密码）转换为乱码形式的字节序列（其实就是字符串）。<br />*async* *def* login_for_access_token(*form_data*: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:<br />*async* *def* read_users_me(*current_user*: Annotated[User, Depends(get_current_active_user)]): |

⚠️ `*async* *def* read_users_me(*current_user*: Annotated[User, Depends(get_current_active_user)]):` 流程

> 客户端请求带上 Header Authorization: Bearer <token>
>
> get_current_user() 中的 Depends(oauth2_scheme) 提取 token
>
> jwt.decode() 解码 token，获取 sub 字段（即用户名）
>
> 调用 get_user(...) 拿到用户数据
>
> get_current_active_user() 检查用户是否已禁用



#### 🎯 中间件

"中间件"是一个函数,它在每个**请求**被特定的*路径操作*处理之前,以及在每个**响应**返回之前工作.

- 它接收的应用程序的每一个**请求**.
- 然后它可以对这个**请求**做一些事情或者执行任何需要的代码.
- 然后它将**请求**传递给应用程序的其他部分 (通过某种*路径操作*).
- 然后它获取应用程序生产的**响应** (通过某种*路径操作*).
- 它可以对该**响应**做些什么或者执行任何需要的代码.
- 然后它返回这个 **响应**.





#### 🎯 CORS（跨域资源共享）

指浏览器中运行的前端拥有与后端通信的 JavaScript 代码，而后端处于与前端不同的「源」的情况。



源是协议（`http`，`https`）、域（`myapp.com`，`localhost`，`localhost.tiangolo.com`）以及端口（`80`、`443`、`8080`）的组合。

因此，这些都是不同的源：

- `http://localhost`
- `https://localhost`
- `http://localhost:8080`

即使它们都在 `localhost` 中，但是它们使用不同的协议或者端口，所以它们都是不同的「源」。



```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
```



#### 🎯 SQL（关系型）数据库

```python
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```





#### 🎯 更大的应用 - 多个文件

```per
 .
├── app                  # 「app」是一个 Python 包
│   ├── __init__.py      # 这个文件使「app」成为一个 Python 包
│   ├── main.py          # 「main」模块，例如 import app.main
│   ├── dependencies.py  # 「dependencies」模块，例如 import app.dependencies
│   └── routers          # 「routers」是一个「Python 子包」
│   │   ├── __init__.py  # 使「routers」成为一个「Python 子包」
│   │   ├── items.py     # 「items」子模块，例如 import app.routers.items
│   │   └── users.py     # 「users」子模块，例如 import app.routers.users
│   └── internal         # 「internal」是一个「Python 子包」
│       ├── __init__.py  # 使「internal」成为一个「Python 子包」
│       └── admin.py     # 「admin」子模块，例如 import app.internal.admin
```



| 名称                        | 功能                                                         |
| --------------------------- | ------------------------------------------------------------ |
| `APIRouter`                 | 可以将 `APIRouter` 视为一个「迷 `FastAPI`」类              |
| 依赖项                      | 我们将需要一些在应用程序的好几个地方所使用的依赖项。将它们放在它们自己的 `dependencies` 模块 |
| 其他使用 `APIRouter` 的模块 | 共同的前缀                                                   |
| `FastAPI` 主体              | 位于 `app/main.py` 的模块                                    |
| 导入                        | `app.include_router`                                         |



#### 🎯 后台任务

可以定义在返回响应后运行的后台任务。

这对需要在请求之后执行的操作很有用，但客户端不必在接收响应之前等待操作完成。

包括这些例子：

- 执行操作后发送的电子邮件通知：
  - 由于连接到电子邮件服务器并发送电子邮件往往很“慢”（几秒钟），您可以立即返回响应并在后台发送电子邮件通知。
- 处理数据：
  - 例如，假设您收到的文件必须经过一个缓慢的过程，您可以返回一个"Accepted"(HTTP 202)响应并在后台处理它。



| 名称                   | 功能                                                         |
| ---------------------- | ------------------------------------------------------------ |
| 使用 `BackgroundTasks` | `from fastapi import BackgroundTasks, FastAPI`               |
| 创建一个任务函数       | `def write_notification(email: str, message="")`             |
| 添加后台任务           | `background_tasks.add_task()`                                |
| 依赖注入               | 使用 `BackgroundTasks` 也适用于依赖注入系统，可以在多个级别声明 `BackgroundTasks` 类型的参数：<br />在 *路径操作函数* 里，在依赖中(可依赖)，在子依赖中，等等。 |
| 技术细节               | `BackgroundTasks` 类直接来自 `starlette.background`          |
| 告诫                   | 如果需要执行繁重的后台计算，并且不一定需要由同一进程运行（例如，不需要共享内存、变量等），<br />那么使用其他更大的工具（如 [Celery](https://docs.celeryq.dev/)）可能更好。 |



#### 🎯 元数据和文档 URL

🧩 API 元数据

```python
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
```

🧩 标签元数据

```python
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

#### 🎯 静态文件

可以使用 `StaticFiles`从目录中自动提供静态文件。

使用`StaticFiles`

- 导入`StaticFiles`。
- "挂载"(Mount) 一个 `StaticFiles()` 实例到一个指定路径。

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
```

这个 "子应用" 会被 "挂载" 到第一个 `"/static"` 指向的子路径。因此，任何以`"/static"`开头的路径都会被它处理。

`directory="static"` 指向包含的静态文件的目录名字。

`name="static"` 提供了一个能被**FastAPI**内部使用的名字。



#### 🎯 测试

🧩 使用 `TestClient`

创建名字以 `test_` 开头的函数（这是标准的 `pytest` 约定）。

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```



 🧩 分离测试

```python
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

 🧩 测试：扩展示例
```perl
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

可以使用扩展后的测试更新`test_main.py`

之后，只需要安装 `pytest`运行起来



#### 🎯 调试

🧩 调用 `uvicorn`，在 FastAPI 应用中直接导入 `uvicorn` 并运行

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

