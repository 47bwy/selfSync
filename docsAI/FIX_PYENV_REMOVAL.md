# 彻底移除 pyenv 指南

即使注释了 `.zshrc` 中的 pyenv 配置，pyenv 可能仍然存在。以下是完整的清理步骤。

## 🔍 问题诊断

你的情况：
- ✅ pyenv 是通过 **Homebrew** 安装的（`/usr/local/bin/pyenv`）
- ✅ pyenv 是一个 **shell 函数**（不是普通的可执行文件）
- ⚠️ 即使注释了 `.zshrc`，当前 shell 会话中仍然有 pyenv 函数

## 🛠️ 解决步骤

### 步骤 1: 检查 Homebrew 安装的 pyenv

```bash
# 检查是否通过 Homebrew 安装
brew list --formula | grep pyenv

# 如果输出包含 pyenv，说明是通过 Homebrew 安装的
```

### 步骤 2: 卸载 Homebrew 的 pyenv

```bash
# 卸载 pyenv
brew uninstall pyenv

# 这也会自动移除 /usr/local/bin/pyenv 的链接
```

### 步骤 3: 清理 pyenv 目录和数据

```bash
# 删除 pyenv 的安装目录
rm -rf ~/.pyenv

# 删除 pyenv 的缓存
rm -rf ~/.pyenv/cache 2>/dev/null || true
```

### 步骤 4: 清理所有配置文件

检查并清理以下文件中的 pyenv 配置：

```bash
# 查看所有可能包含 pyenv 的配置文件
grep -r "pyenv" ~/.zshrc ~/.zprofile ~/.zshenv ~/.bash_profile ~/.bashrc 2>/dev/null

# 手动编辑并删除/注释所有 pyenv 相关行
```

**需要删除的典型配置行**：
```bash
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"  # 或 eval "$(pyenv init - bash)"
eval "$(pyenv init --path)"
```

### 步骤 5: 清理 shell 函数（重要！）

当前打开的终端中，pyenv 函数仍然在内存中。需要：

**方法 A: 重启终端**（最简单）
- 完全关闭当前终端
- 打开新终端

**方法 B: 重新加载 shell**
```bash
# 重新启动 zsh
exec zsh

# 或者
source ~/.zshrc
```

**方法 C: 手动取消定义函数**
```bash
# 在当前终端中取消定义 pyenv 函数
unset -f pyenv

# 验证
type pyenv
# 应该显示：pyenv: not found
```

### 步骤 6: 清理 PATH 中的 pyenv shims

```bash
# 检查 PATH 中是否还有 pyenv shims
echo $PATH | tr ':' '\n' | grep pyenv

# 如果有，需要从配置文件中删除相关 PATH 配置
```

### 步骤 7: 验证清理结果

**打开新的终端窗口**（重要！），然后：

```bash
# 检查 pyenv 是否还存在
which pyenv
# 应该显示：pyenv not found

type pyenv
# 应该显示：pyenv: not found

pyenv --version
# 应该显示：command not found

# 检查 PATH
echo $PATH | grep pyenv
# 应该没有任何输出
```

### 步骤 8: 清理残留文件（可选）

```bash
# 检查是否有其他 pyenv 相关文件
find ~ -name "*pyenv*" -type f 2>/dev/null
find ~ -name "*pyenv*" -type d 2>/dev/null

# 根据输出决定是否删除
```

---

## 📝 一键清理脚本

创建一个更完整的清理脚本：

```bash
#!/bin/bash

echo "开始彻底清理 pyenv..."

# 1. 卸载 Homebrew 的 pyenv
if brew list --formula | grep -q "^pyenv$"; then
    echo "[1/6] 卸载 Homebrew pyenv..."
    brew uninstall pyenv
    echo "  ✓ 已卸载"
else
    echo "[1/6] Homebrew pyenv 未安装"
fi

# 2. 删除 pyenv 目录
if [ -d ~/.pyenv ]; then
    echo "[2/6] 删除 ~/.pyenv 目录..."
    rm -rf ~/.pyenv
    echo "  ✓ 已删除"
else
    echo "[2/6] ~/.pyenv 目录不存在"
fi

# 3. 清理配置文件中的 pyenv
echo "[3/6] 清理配置文件..."
for file in ~/.zshrc ~/.zprofile ~/.zshenv ~/.bash_profile ~/.bashrc; do
    if [ -f "$file" ]; then
        # 备份原文件
        cp "$file" "${file}.backup-$(date +%Y%m%d-%H%M%S)"
        # 删除 pyenv 相关行（注释掉的也删除）
        sed -i '' '/pyenv/d' "$file" 2>/dev/null || sed -i '/pyenv/d' "$file" 2>/dev/null
        echo "  ✓ 已清理 $file"
    fi
done

# 4. 清理 PATH 中的 pyenv
echo "[4/6] 清理 PATH..."
# PATH 清理需要在配置文件中完成，上面已处理

# 5. 检查残留
echo "[5/6] 检查残留..."
if command -v pyenv &> /dev/null; then
    echo "  ⚠️  警告：pyenv 命令仍然存在"
    echo "  请关闭终端并重新打开，或运行: exec zsh"
else
    echo "  ✓ pyenv 命令已移除"
fi

# 6. 提示
echo "[6/6] 完成！"
echo ""
echo "下一步："
echo "  1. 关闭当前终端并打开新终端（重要！）"
echo "  2. 验证: which pyenv （应该显示 not found）"
echo "  3. 安装 UV: curl -LsSf https://astral.sh/uv/install.sh | sh"
```

---

## ✅ 完整清理清单

按顺序执行：

- [ ] 卸载 Homebrew pyenv: `brew uninstall pyenv`
- [ ] 删除 pyenv 目录: `rm -rf ~/.pyenv`
- [ ] 编辑配置文件，删除/注释所有 pyenv 相关行
- [ ] 在当前终端取消函数: `unset -f pyenv`（临时）
- [ ] **关闭并重新打开终端**（必需！）
- [ ] 验证清理结果: `which pyenv`（应该显示 not found）
- [ ] 检查 PATH: `echo $PATH | grep pyenv`（应该无输出）

---

## 🎯 快速修复命令

如果你想立即在当前终端中禁用 pyenv（无需重启）：

```bash
# 1. 卸载 Homebrew pyenv
brew uninstall pyenv

# 2. 删除 pyenv 目录
rm -rf ~/.pyenv

# 3. 取消定义 pyenv 函数（仅对当前会话有效）
unset -f pyenv

# 4. 从 PATH 中移除 pyenv shims（仅对当前会话有效）
export PATH=$(echo $PATH | tr ':' '\n' | grep -v pyenv | tr '\n' ':')

# 5. 验证
which pyenv
type pyenv
```

**注意**：这只是临时禁用。要永久移除，必须：
1. 清理配置文件
2. **关闭并重新打开终端**

---

## ⚠️ 为什么注释了配置还有 pyenv？

原因：
1. **Shell 函数已加载**：pyenv 是一个 shell 函数，已经加载到当前会话的内存中
2. **Homebrew 自动配置**：通过 Homebrew 安装的 pyenv 可能在其他地方也有配置
3. **多个配置文件**：可能在其他配置文件（如 `.zprofile`, `.zshenv`）中也有配置

解决方法：
- **必须关闭并重新打开终端**，让新的配置生效
- 或者使用 `exec zsh` 重新启动 shell

---

## 🚀 清理完成后

清理完成后，按照 `CLEAN_PYTHON_AND_SETUP_UV.md` 的步骤安装和使用 UV。

