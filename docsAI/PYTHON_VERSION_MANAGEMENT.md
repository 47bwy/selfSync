# macOS Python 版本管理指南

本文档说明在 macOS 上管理 Python 版本的最佳实践。

## 🎯 推荐方案：UV（统一管理）

由于项目已迁移到 UV，**强烈推荐使用 UV 管理 Python 版本**，这样可以：
- ✅ 统一使用一个工具（版本管理 + 包管理）
- ✅ 项目级别自动 Python 版本管理
- ✅ 极速安装和切换
- ✅ 无需额外配置

### 安装 Python 版本

```bash
# 安装指定版本的 Python
uv python install 3.11
uv python install 3.12
uv python install 3.13

# 安装最新版本
uv python install

# 列出所有可安装的版本
uv python list

# 列出已安装的版本
uv python list --installed
```

### 为项目指定 Python 版本

在 `pyproject.toml` 中已经指定了：

```toml
[project]
requires-python = ">=3.11"
```

UV 会自动：
- 检查是否需要安装指定的 Python 版本
- 为项目创建使用该版本的虚拟环境
- 自动切换和隔离不同项目的 Python 版本

### 使用项目时

```bash
# 进入项目目录，UV 会自动使用正确的 Python 版本
cd /Users/apri/Documents/selfSync

# 同步依赖（会自动安装/使用 Python 3.11）
uv sync

# 运行 Python（自动使用项目指定的版本）
uv run python open_urls.py
```

### 手动指定 Python 版本

```bash
# 使用特定版本运行
uv run --python 3.12 python script.py

# 临时使用特定版本
uv python pin 3.12
```

### 查看当前使用的 Python

```bash
# 查看 UV 管理的 Python 版本
uv python list

# 查看项目使用的 Python 版本
uv run python --version
```

---

## 备选方案：pyenv（最成熟）

如果你需要更细粒度的控制，或者与其他工具集成，可以使用 pyenv。

### 安装 pyenv

```bash
# 使用 Homebrew 安装（推荐）
brew install pyenv

# 配置 shell（添加到 ~/.zshrc 或 ~/.bash_profile）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

### 基本使用

```bash
# 安装 Python 版本
pyenv install 3.11.9
pyenv install 3.12.4
pyenv install 3.13.0

# 查看已安装的版本
pyenv versions

# 设置全局版本
pyenv global 3.12.4

# 为项目设置本地版本
cd /path/to/project
pyenv local 3.11.9

# 查看当前使用的版本
pyenv version
```

### 为项目设置版本

```bash
# 在项目根目录创建 .python-version 文件
cd /Users/apri/Documents/selfSync
pyenv local 3.11

# 这会创建一个 .python-version 文件
```

### 常见问题

```bash
# Python 安装失败（缺少依赖）
# 安装必要的编译工具
xcode-select --install
brew install openssl readline sqlite3 xz zlib tcl-tk

# 查看可安装的版本
pyenv install --list
```

---

## 方案对比

| 特性 | UV | pyenv | Homebrew |
|------|-----|-------|----------|
| **速度** | ⚡⚡⚡ 极快 | 🐢 较慢 | 🐢 较慢 |
| **项目级别管理** | ✅ 自动 | ✅ 支持 | ❌ 不支持 |
| **统一工具** | ✅ 版本+包管理 | ❌ 仅版本管理 | ❌ 仅安装 |
| **易用性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **成熟度** | 🆕 较新 | ⭐⭐⭐⭐⭐ 最成熟 | ⭐⭐⭐⭐ |
| **推荐场景** | 现代项目 | 传统项目/多工具 | 简单场景 |

---

## 🎯 推荐方案：UV

### 为什么推荐 UV？

1. **统一管理**：一个工具搞定版本管理和包管理
2. **项目自动管理**：根据 `pyproject.toml` 自动处理
3. **速度快**：安装和切换都很快
4. **现代化**：符合最新 Python 生态系统标准

### 实际操作示例

```bash
# 1. 安装 UV（如果还没安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 进入项目目录
cd /Users/apri/Documents/selfSync

# 3. 同步依赖（UV 会自动检查并安装 Python 3.11）
uv sync

# 4. 运行项目（自动使用正确的 Python 版本）
uv run python open_urls.py -f url.md -k your-key

# 5. 如果需要其他 Python 版本做测试
uv python install 3.12
uv run --python 3.12 python script.py
```

---

## ⚠️ 注意事项

### 1. 不要使用系统自带的 Python

macOS 自带的 Python 可能：
- 版本过旧
- 系统组件依赖，不应该修改
- 缺少某些功能

**解决方案**：始终使用 UV 或 pyenv 管理的 Python

### 2. Homebrew 的 Python

```bash
# Homebrew 也可以安装 Python，但不推荐用于版本管理
brew install python@3.11 python@3.12

# 问题：
# - 难以在版本间切换
# - 可能与系统 Python 冲突
# - 管理多个版本较麻烦
```

### 3. 项目级别的版本管理

**UV（推荐）**：
- 自动根据 `pyproject.toml` 的 `requires-python` 使用正确的版本
- 每个项目独立虚拟环境

**pyenv**：
- 需要在项目目录创建 `.python-version` 文件
- 需要配合虚拟环境工具使用

---

## 📚 相关命令速查

### UV

```bash
# Python 版本管理
uv python install <version>      # 安装 Python 版本
uv python list                   # 列出可用版本
uv python list --installed       # 列出已安装版本
uv python pin <version>          # 固定项目 Python 版本

# 运行项目
uv run python script.py          # 使用项目 Python 运行
uv run --python 3.12 script.py   # 使用指定版本运行
uv sync                          # 同步依赖（自动检查 Python 版本）
```

### pyenv

```bash
# Python 版本管理
pyenv install <version>          # 安装 Python 版本
pyenv uninstall <version>        # 卸载 Python 版本
pyenv versions                   # 列出已安装版本
pyenv version                    # 显示当前版本

# 版本切换
pyenv global <version>           # 设置全局版本
pyenv local <version>            # 设置项目本地版本
pyenv shell <version>            # 设置当前 shell 版本

# 其他
pyenv rehash                     # 重建 shims（安装新包后）
pyenv which python               # 显示 Python 可执行文件路径
```

---

## ✅ 总结

**推荐使用 UV**，因为：
1. 你已经在使用 UV 进行包管理
2. 统一工具，减少学习成本
3. 项目级别自动管理，无需手动配置
4. 速度快，体验好

**迁移到 UV 的 Python 管理后，你不再需要 pyenv**！

---

## 🔗 参考资源

- [UV 官方文档 - Python 管理](https://docs.astral.sh/uv/python/)
- [pyenv 官方文档](https://github.com/pyenv/pyenv)
- [Python.org - macOS 指南](https://docs.python.org/zh-cn/dev/using/mac.html)

