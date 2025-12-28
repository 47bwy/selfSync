# macOS Python 清理与 UV 安装指南

本文档将帮助你彻底清理 macOS 上的 Python 安装，然后使用 UV 进行统一管理。

## 📋 目录

1. [关于 UV 和 Python 的误解](#关于-uv-和-python-的误解)
2. [清理现有 Python 安装](#清理现有-python-安装)
3. [安装 UV](#安装-uv)
4. [使用 UV 管理 Python](#使用-uv-管理-python)
5. [验证和测试](#验证和测试)

---

## 关于 UV 和 Python 的误解

### ❓ 问题：`brew install uv` 会用 Python 构建吗？

**答案：不会！**

1. **UV 是用 Rust 编写的**，不依赖 Python 来构建
2. `brew install uv` 安装的是**预编译的二进制文件**，不需要编译
3. 即使从源码编译，也是用 Rust 编译器（`rustc`），不是 Python

### ✅ 推荐安装方式

**使用官方安装脚本**（推荐）：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

这种方式：
- ✅ 不依赖任何现有的 Python 安装
- ✅ 直接下载预编译的二进制文件
- ✅ 自动配置 PATH
- ✅ 最快最干净

**备选：Homebrew**
```bash
brew install uv
```
虽然也可以用，但不如官方脚本直接。

---

## 清理现有 Python 安装

### 步骤 1: 检查所有 Python 安装

先运行以下命令检查当前状态：

```bash
# 查看所有 python 可执行文件
which -a python python3

# 查看 pyenv 安装的版本
ls -la ~/.pyenv/versions

# 查看 Homebrew 安装的 Python
brew list --formula | grep -i python

# 查看 pip 安装位置
pip --version 2>/dev/null || pip3 --version

# 查看虚拟环境
ls -la ~/.virtualenvs 2>/dev/null || echo "No virtualenvs"
```

### 步骤 2: 备份重要数据（可选）

如果你有重要的项目或虚拟环境，先备份：

```bash
# 备份 pip 已安装的包列表
pip3 list --format=freeze > ~/python_packages_backup.txt 2>/dev/null || true

# 备份 pyenv 的版本（如果需要）
# 注意：pyenv 版本可以重新安装，主要是备份项目依赖
```

### 步骤 3: 卸载 pyenv 及其 Python 版本

```bash
# 1. 卸载 pyenv 管理的所有 Python 版本
pyenv uninstall -f 3.8.5
pyenv uninstall -f 3.10.13
pyenv uninstall -f 3.11.9

# 或者删除整个 pyenv 目录
rm -rf ~/.pyenv

# 2. 从 shell 配置中移除 pyenv
# 编辑 ~/.zshrc（如果使用 zsh）或 ~/.bash_profile（如果使用 bash）
# 删除或注释掉以下行：
#   export PYENV_ROOT="$HOME/.pyenv"
#   command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
#   eval "$(pyenv init - zsh)"  # 或 eval "$(pyenv init - bash)"

# 3. 重新加载 shell 配置
source ~/.zshrc  # 或 source ~/.bash_profile
```

### 步骤 4: 卸载 Homebrew 安装的 Python

```bash
# 查看所有 Python 相关包
brew list --formula | grep -i python

# 卸载所有 Python 版本
brew uninstall --ignore-dependencies python@3.14
brew uninstall --ignore-dependencies python@3.12 2>/dev/null || true
brew uninstall --ignore-dependencies python@3.11 2>/dev/null || true
brew uninstall --ignore-dependencies python@3.10 2>/dev/null || true
brew uninstall --ignore-dependencies python@3.9 2>/dev/null || true

# 清理 Homebrew 缓存
brew cleanup -s python@*
```

### 步骤 5: 清理 pip 缓存和用户包

```bash
# 清理 pip 缓存
pip3 cache purge 2>/dev/null || true

# 删除用户级别的 pip 包（可选，如果需要彻底清理）
# 注意：这会删除所有用户安装的 Python 包
# rm -rf ~/.local/lib/python3.*
# rm -rf ~/.local/bin/*pip*
```

### 步骤 6: 清理虚拟环境

```bash
# 如果你使用 virtualenv/venv
rm -rf ~/.virtualenvs 2>/dev/null || true

# 清理项目中的虚拟环境
find ~ -name ".venv" -type d -exec rm -rf {} + 2>/dev/null || true
find ~ -name "venv" -type d -exec rm -rf {} + 2>/dev/null || true
find ~ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
```

### 步骤 7: 清理 PATH 中的 Python 引用

```bash
# 检查 PATH 中是否有 Python 相关路径
echo $PATH | tr ':' '\n' | grep -i python

# 编辑 ~/.zshrc 或 ~/.bash_profile
# 删除所有 Python、pyenv、pip 相关的 PATH 配置
```

### ⚠️ 重要：不要删除系统 Python

**不要删除** `/usr/bin/python3`，因为：
- 这是 macOS 系统自带的 Python
- 系统组件可能依赖它
- 通常版本较旧，但不影响使用 UV

**解决方案**：忽略它，让 UV 管理的 Python 优先级更高。

### 步骤 8: 验证清理结果

```bash
# 检查 Python 可执行文件
which -a python python3

# 应该只剩下：
# /usr/bin/python3  （系统 Python，保留）
# 可能还有 pyenv shims（如果没删除 pyenv）

# 检查 pyenv
pyenv --version 2>/dev/null || echo "pyenv removed ✓"

# 检查 Homebrew Python
brew list --formula | grep -i python || echo "Homebrew Python removed ✓"
```

---

## 安装 UV

### 方法 1: 官方安装脚本（推荐）⭐

```bash
# 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 重新加载 shell 配置（脚本会自动添加到 ~/.zshrc 或 ~/.bash_profile）
source ~/.zshrc  # 或 source ~/.bash_profile

# 验证安装
uv --version
```

### 方法 2: Homebrew（备选）

```bash
brew install uv
uv --version
```

### 方法 3: 使用 pip（不推荐，但可以作为临时方案）

```bash
# 如果系统有 Python（通常 macOS 有 /usr/bin/python3）
/usr/bin/python3 -m pip install --user uv

# 添加到 PATH
export PATH="$HOME/.local/bin:$PATH"
```

---

## 使用 UV 管理 Python

### 安装 Python 版本

```bash
# 安装项目需要的 Python 3.11
uv python install 3.11

# 安装其他版本（可选）
uv python install 3.12
uv python install 3.13

# 查看已安装的版本
uv python list --installed

# 查看所有可用版本
uv python list
```

### 设置项目 Python 版本

你的项目已经在 `pyproject.toml` 中指定了：

```toml
requires-python = ">=3.11"
```

进入项目目录并同步：

```bash
cd /Users/apri/Documents/selfSync

# UV 会自动检查并安装 Python 3.11（如果还没安装）
uv sync

# 验证使用的 Python 版本
uv run python --version
# 应该显示 Python 3.11.x
```

### 配置 shell（可选）

如果你想让 `python` 命令默认使用 UV 管理的版本：

```bash
# 添加到 ~/.zshrc 或 ~/.bash_profile
eval "$(uv tool run --python 3.11 --command python --version 2>/dev/null || echo '')"

# 或者创建一个 alias
alias python='uv run python'
alias python3='uv run python'
```

---

## 验证和测试

### 1. 验证 UV 安装

```bash
uv --version
uv python list
```

### 2. 验证 Python 安装

```bash
# 使用 UV 安装的 Python
uv run python --version

# 应该显示 Python 3.11.x（或你安装的版本）
```

### 3. 测试项目

```bash
cd /Users/apri/Documents/selfSync

# 同步依赖
uv sync

# 运行项目脚本
uv run python open_urls.py --help

# 运行 mkdocs
uv run mkdocs --version
```

### 4. 检查环境隔离

```bash
# 查看虚拟环境位置（UV 自动创建）
uv run python -c "import sys; print(sys.prefix)"

# 查看安装的包
uv pip list
```

---

## 完整清理脚本

如果你想一键执行大部分清理操作（**请先备份重要数据**）：

```bash
#!/bin/bash
# 清理脚本 - 谨慎使用！

echo "开始清理 Python 安装..."

# 1. 卸载 pyenv Python 版本
if command -v pyenv &> /dev/null; then
    echo "卸载 pyenv Python 版本..."
    pyenv versions --bare | xargs -I {} pyenv uninstall -f {}
fi

# 2. 卸载 Homebrew Python
echo "卸载 Homebrew Python..."
brew uninstall --ignore-dependencies python@3.14 2>/dev/null || true
brew uninstall --ignore-dependencies python@3.12 2>/dev/null || true
brew uninstall --ignore-dependencies python@3.11 2>/dev/null || true
brew uninstall --ignore-dependencies python@3.10 2>/dev/null || true
brew cleanup -s python@*

# 3. 清理 pip 缓存
echo "清理 pip 缓存..."
pip3 cache purge 2>/dev/null || true

echo "清理完成！"
echo "现在可以安装 UV: curl -LsSf https://astral.sh/uv/install.sh | sh"
```

**⚠️ 警告**：这个脚本会删除所有通过 pyenv 和 Homebrew 安装的 Python，请确保你不需要它们。

---

## 常见问题

### Q: 清理后系统 Python 还能用吗？

A: 可以，系统 Python (`/usr/bin/python3`) 不会被删除，但建议使用 UV 管理的 Python。

### Q: 如果某些工具依赖特定版本的 Python 怎么办？

A: UV 可以为每个项目自动使用正确的 Python 版本，或者使用 `uv run --python <version>` 指定版本。

### Q: pyenv 还需要保留吗？

A: 不需要。UV 可以完全替代 pyenv。如果确定不再需要，可以完全卸载：

```bash
# 删除 pyenv
rm -rf ~/.pyenv

# 从 shell 配置中删除 pyenv 相关行
# 编辑 ~/.zshrc，删除 pyenv 相关配置
```

### Q: 清理后如何恢复？

A: 如果清理后发现问题，可以：
1. 使用 UV 重新安装需要的 Python 版本
2. 使用 Homebrew 重新安装（如果需要）

### Q: UV 管理的 Python 在哪里？

A: UV 将 Python 安装在 `~/.uv/python/` 目录下，每个版本独立管理。

---

## ✅ 清理检查清单

- [ ] 备份重要项目依赖（如果有）
- [ ] 卸载 pyenv 的 Python 版本
- [ ] 卸载 Homebrew 的 Python 版本
- [ ] 清理 pip 缓存
- [ ] 清理虚拟环境
- [ ] 从 shell 配置中移除 pyenv
- [ ] 验证清理结果
- [ ] 安装 UV
- [ ] 使用 UV 安装 Python 3.11
- [ ] 测试项目运行

---

## 🎯 总结

1. **清理步骤**：先清理 pyenv 和 Homebrew 的 Python
2. **安装 UV**：使用官方脚本 `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **UV 不依赖 Python**：它是 Rust 编写的，无需 Python 即可安装
4. **统一管理**：之后所有 Python 版本和包都通过 UV 管理

完成这些步骤后，你的 Python 环境将变得干净、统一、易于管理！

