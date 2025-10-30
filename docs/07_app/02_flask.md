# Flask 精华速查

## 1. Flask 简介
- 轻量级 Python Web 框架，核心简单、易扩展，适合中小型及可扩展大型应用。
- 遵循 WSGI 标准，生态丰富。

## 2. 安装
```bash
pip install Flask
```

## 3. 快速入门
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

## 4. 路由与视图
- `@app.route("/path")` 设定 URL 路由，支持变量路径：`/user/<username>`

## 5. 请求与响应
```python
from flask import request, jsonify, make_response

# 获取参数
request.args.get("username")     # GET
request.form["password"]         # POST
request.get_json()               # JSON body

# 返回 JSON
return jsonify({"msg": "ok"})
```

## 6. 模板渲染
- 用 Jinja2，模板放 `templates/`。
```python
from flask import render_template
@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)
```

## 7. 静态文件
- 静态资源放 `static/`，模板中 `{{ url_for('static', filename='style.css') }}`

## 8. 表单和文件上传
- `request.form`、`request.files` 获取表单和上传文件。

## 9. Session、Cookie、配置
```python
from flask import session

app.secret_key = "your_secret_key"
session["user_id"] = 123
user_id = session.get("user_id")

# 配置
app.config["DEBUG"] = True
```

## 10. 错误处理
```python
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
```

## 11. 蓝图 Blueprint
- 用于模块化大型应用。
```python
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route("/")
def admin_home():
    return "Admin"
app.register_blueprint(bp)
```

## 12. 数据库集成
- 推荐 Flask-SQLAlchemy：
```python
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)
```

## 13. 常用扩展
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (迁移)
- Flask-Login (认证)
- Flask-WTF (表单)
- Flask-RESTful (API)
- Flask-CORS (跨域)

---

## 14. 用户认证机制

### a. 使用 Flask-Login（登录态认证）
```python
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user

login_manager = LoginManager(app)

class User(UserMixin):
    # 必须实现 get_id 方法
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    user = User.query.filter_by(username=request.form["username"]).first()
    if user and check_password(user, request.form["password"]):
        login_user(user)
        return "登录成功"
    return "用户名或密码错误"

@app.route("/protected")
@login_required
def protected():
    return f"当前用户: {current_user.username}"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "已登出"
```
- 提供用户 session 登录、登出、权限检查。

### b. 基于 Token/JWT 的认证（常用于API）
```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.json.get("username")
    # ...校验逻辑
    token = create_access_token(identity=username)
    return jsonify(access_token=token)

@app.route("/api/protected")
@jwt_required()
def api_protected():
    user = get_jwt_identity()
    return f"当前用户: {user}"
```
- 适合前后端分离、移动端应用。

---

## 15. 配置与环境
- 配置可用 `.env`、环境变量、`app.config.from_pyfile()`。
- 常用环境变量：`FLASK_ENV=development`、`FLASK_DEBUG=1`

## 16. 常用开发命令
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## 17. 热加载与调试
- `debug=True` 或 `FLASK_ENV=development` 时自动热重载。

## 18. 跨域支持
- 用 Flask-CORS 扩展快速实现跨域
```python
from flask_cors import CORS
CORS(app)
```

## 19. 日志与中间件
- 使用 `app.before_request`、`app.after_request` 实现请求拦截、日志记录。

## 20. 部署建议
- 生产环境不要用自带服务器，推荐 Gunicorn、uWSGI。
- 配合 Nginx、Docker 部署。

---

## 21. 其它进阶要点
- 请求钩子（before/after_request）自定义处理。
- RESTful API 支持，可用 Flask-RESTful、Marshmallow（序列化）。
- 支持单元测试：`flask.testing.FlaskClient`
- 支持 WebSocket 可用 Flask-SocketIO。

---

> **速查建议**：掌握路由、请求响应、模板、Session、蓝图、数据库、认证机制、错误处理、配置、开发调试、部署等核心用法。查[官方文档](https://flask.palletsprojects.com/)获取更多信息。