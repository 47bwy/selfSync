# 从 Pipenv 迁移到 UV 指南

本文档将指导你如何将项目从 Pipenv 迁移到 UV。

## 📋 目录

1. [安装 UV](#1-安装-uv)
2. [迁移步骤](#2-迁移步骤)
3. [常用命令对比](#3-常用命令对比)
4. [验证迁移](#4-验证迁移)
5. [清理旧文件](#5-清理旧文件)

---

## 1. 安装 UV

### macOS / Linux

```bash
# 使用官方安装脚本（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 Homebrew (macOS)
brew install uv

# 或使用 pip
pip install uv
```

### 验证安装

```bash
uv --version
```

---

## 2. 迁移步骤

### 步骤 1: 初始化 UV 项目

在项目根目录执行：

```bash
# 初始化项目（会创建 pyproject.toml）
uv init --python 3.11

# 或者如果 pyproject.toml 已存在，直接使用
uv sync
```

### 步骤 2: 从 Pipfile 添加依赖

如果你已经创建了 `pyproject.toml`，可以直接使用：

```bash
# 安装所有依赖
uv sync
```

或者手动添加依赖：

```bash
# 添加单个包
uv add package-name

# 添加带版本约束的包
uv add "package-name==1.0.0"

# 添加开发依赖
uv add --dev package-name
```

### 步骤 3: 创建虚拟环境并安装依赖

```bash
# UV 会自动创建虚拟环境并安装依赖
uv sync

# 这会：
# 1. 创建虚拟环境（如果不存在）
# 2. 安装 pyproject.toml 中定义的所有依赖
# 3. 生成 uv.lock 锁定文件
```

---

## 3. 常用命令对比

### 虚拟环境管理

| Pipenv | UV | 说明 |
|--------|----|----|
| `pipenv shell` | `uv shell` | 激活虚拟环境 |
| `pipenv install` | `uv sync` | 安装依赖 |
| `pipenv install package` | `uv add package` | 添加新包 |
| `pipenv install --dev package` | `uv add --dev package` | 添加开发依赖 |
| `pipenv uninstall package` | `uv remove package` | 移除包 |
| `pipenv update` | `uv sync --upgrade` | 更新依赖 |
| `pipenv lock` | `uv lock` | 更新锁定文件 |
| `pipenv graph` | `uv tree` | 查看依赖树 |

### 运行脚本

| Pipenv | UV | 说明 |
|--------|----|----|
| `pipenv run python script.py` | `uv run python script.py` | 在虚拟环境中运行 |
| `pipenv run command` | `uv run command` | 运行任意命令 |

### 其他常用命令

```bash
# 查看已安装的包
uv pip list

# 查看依赖树
uv tree

# 更新所有依赖到最新版本
uv sync --upgrade

# 只更新锁定文件，不安装
uv lock --upgrade

# 清理缓存
uv cache clean

# 查看项目信息
uv project info
```

---

## 4. 验证迁移

### 检查依赖是否正确安装

```bash
# 检查虚拟环境中的包
uv pip list

# 运行项目脚本测试
uv run python open_urls.py --help
```

### 验证项目功能

```bash
# 测试主要功能
uv run python open_urls.py -f url.md -k your-key

# 如果使用 mkdocs
uv run mkdocs serve
```

---

## 5. 清理旧文件

迁移完成后，可以删除以下文件：

```bash
# 删除 Pipenv 相关文件
rm Pipfile
rm Pipfile.lock

# 删除 requirements.txt（如果不再需要）
rm requirements.txt

# 删除旧的虚拟环境（如果存在）
rm -rf .venv  # Pipenv 默认使用 .venv
```

**注意**：建议先验证项目完全正常后再删除旧文件。

---

## 📝 pyproject.toml 说明

UV 使用标准的 `pyproject.toml` 文件（符合 PEP 621）。以下是各个部分的详细说明和最佳实践。

### 1. `[project]` 部分

这是项目的核心配置部分：

```toml
[project]
name = "selfsync"              # 项目名称（必需）
version = "0.1.0"              # 项目版本（必需，遵循语义化版本）
description = "项目描述"       # 项目简短描述（可选）
readme = "README.md"           # README 文件路径（可选）
requires-python = "==3.10.13"  # Python 版本要求（可选，但强烈推荐）
dependencies = [               # 核心依赖列表（必需）
    "pycryptodome",
    "mkdocs>=1.6.0",
]
```

**关键说明**：
- `name`: 项目标识符，用于包管理和分发
- `version`: 版本号，格式建议使用 `x.y.z`
- `requires-python`: 
  - `==3.10.13` - 固定版本（不推荐，除非有特殊需求）
  - `>=3.11` - 最低版本要求（推荐）
  - `>=3.11,<3.12` - 版本范围
- `dependencies`: 项目运行所需的**核心依赖**，执行 `uv sync` 时会自动安装

### 2. `[project.optional-dependencies]` 部分

可选依赖组，用于按需安装不同的依赖集合：

```toml
[project.optional-dependencies]
examples = [        # 示例代码依赖组
    "numpy>=2.0.0",
    "matplotlib>=3.10.0",
]

dev = [            # 开发依赖组
    "pytest>=7.0.0",
    "black>=23.0.0",
]
```

**如何安装可选依赖**：

```bash
# 安装核心依赖 + 指定可选依赖组
uv sync --extra examples          # 安装 core + examples 组
uv sync --extra dev               # 安装 core + dev 组
uv sync --extra examples --extra dev  # 安装 core + examples + dev

# 或者使用别名
uv sync --extra examples,dev      # 安装多个组（逗号分隔）

# 查看已安装的包
uv pip list
```

**使用场景**：
- `examples`: 运行示例代码需要的依赖（如 numpy, matplotlib）
- `dev`: 开发工具依赖（如测试框架、代码格式化工具）
- `docs`: 文档构建依赖
- `test`: 测试环境依赖

**最佳实践**：
- 只将**必需**的依赖放在 `dependencies`
- 将**可选**的功能依赖分组放在 `optional-dependencies`
- 避免在 `dependencies` 中包含开发工具

### 3. `[build-system]` 部分（可选）

用于定义如何构建和打包项目：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**什么时候需要 `[build-system]`？**

**需要打包的场景**（需要 `[build-system]`）：
- ✅ 开发 **Python 库/包**，要发布到 PyPI
- ✅ 项目需要被其他项目作为依赖安装
- ✅ 使用 `pip install -e .` 进行可编辑安装
- ✅ 需要构建 wheel 或 sdist 分发包

**不需要打包的场景**（可以省略 `[build-system]`）：
- ✅ 纯应用项目（如 CLI 工具、脚本集合）
- ✅ 文档项目（如 MkDocs 站点）
- ✅ 仅用于依赖管理的项目
- ✅ 不需要被其他项目导入的项目

**当前项目示例**：

```toml
# 场景 1: 应用项目（不需要打包）
# 可以完全省略 [build-system]
[project]
name = "selfsync"
dependencies = [...]
# 没有 [build-system]，UV 仍然可以管理依赖

# 场景 2: 库项目（需要打包）
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/selfsync"]  # 指定要打包的包目录
```

**常见问题**：

如果项目没有 `src/` 或 `selfsync/` 目录，但定义了 `[build-system]`，可能会报错：

```
ValueError: Unable to determine which files to ship inside the wheel
```

**解决方案**：
1. **方案一**（推荐）：对于应用项目，移除 `[build-system]`
2. **方案二**：配置 hatchling 不打包任何文件：
   ```toml
   [tool.hatch.build.targets.wheel]
   packages = []  # 空列表，不打包任何代码
   ```

### 4. `[tool.uv]` 部分

UV 特定的配置：

```toml
[tool.uv]
dev-dependencies = []  # UV 的开发依赖（已弃用，使用 optional-dependencies 的 dev 组）

[tool.uv.sources]
# 配置包源（如使用国内镜像）
pypi = { url = "https://pypi.tuna.tsinghua.edu.cn/simple", default = true }
```

**注意**：`dev-dependencies` 已弃用，推荐使用 `[project.optional-dependencies]` 的 `dev` 组。

### 完整配置示例

**应用项目**（当前项目类型）：
```toml
[project]
name = "selfsync"
version = "0.1.0"
description = "Personal knowledge base and utilities"
requires-python = ">=3.11"
dependencies = [
    "pycryptodome",
    "mkdocs>=1.6.0",
]

[project.optional-dependencies]
examples = [
    "numpy>=2.0.0",
    "matplotlib>=3.10.0",
]
dev = [
    "pytest>=7.0.0",
]

# 不需要 [build-system]，因为这是应用项目
```

**库项目**（需要打包）：
```toml
[project]
name = "mylibrary"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.28.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mylibrary"]  # 指定包的位置
```

### 依赖安装命令总结

```bash
# 1. 仅安装核心依赖
uv sync

# 2. 安装核心依赖 + 指定可选依赖组
uv sync --extra examples
uv sync --extra dev
uv sync --extra examples,dev

# 3. 添加新的可选依赖
uv add --optional examples numpy
uv add --optional dev pytest

# 4. 查看依赖树
uv tree

# 5. 查看已安装的包
uv pip list
```

---

## 🚀 UV 的优势

1. **极速安装**：比 pip 快 10-100 倍
2. **一体化工具**：包管理、虚拟环境、项目管理
3. **现代化**：符合 PEP 621 标准
4. **更好的依赖解析**：快速且准确
5. **Python 版本管理**：内置 Python 版本管理

---

## ❓ 常见问题

### Q: 如何指定 Python 版本？

```bash
# 在 pyproject.toml 中指定
requires-python = ">=3.11"

# 或使用 UV 安装特定 Python 版本
uv python install 3.11
```

### Q: 如何迁移现有的虚拟环境？

UV 会自动创建新的虚拟环境。你可以：

1. 删除旧的虚拟环境
2. 运行 `uv sync` 创建新的

### Q: 如何配置国内镜像源？

在 `pyproject.toml` 中添加：

```toml
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

或在命令行：

```bash
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple package-name
```

### Q: 如何导出依赖到 requirements.txt？

```bash
# 导出所有依赖
uv pip compile pyproject.toml -o requirements.txt

# 导出开发依赖
uv pip compile pyproject.toml --extra dev -o requirements-dev.txt
```

---

## 📚 参考资源

- [UV 官方文档](https://docs.astral.sh/uv/)
- [PEP 621 - 项目元数据](https://peps.python.org/pep-0621/)
- [pyproject.toml 规范](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

---

## ✅ 迁移检查清单

- [ ] 安装 UV
- [ ] 创建/更新 `pyproject.toml`
- [ ] 运行 `uv sync` 安装依赖
- [ ] 验证项目功能正常
- [ ] 测试主要脚本
- [ ] 删除旧文件（Pipfile, Pipfile.lock, requirements.txt）
- [ ] 更新 README 中的命令说明（如果有）

---

**迁移完成后，享受 UV 带来的极速体验！** 🎉

