#!/bin/bash
# macOS Python 清理脚本
# 谨慎使用！请先备份重要数据

set -e

echo "=========================================="
echo "macOS Python 清理脚本"
echo "=========================================="
echo ""
echo "⚠️  警告：此脚本将删除以下内容："
echo "  - pyenv 安装的所有 Python 版本"
echo "  - Homebrew 安装的所有 Python 版本"
echo "  - pip 缓存"
echo ""
read -p "是否继续？(输入 YES 确认): " confirm

if [ "$confirm" != "YES" ]; then
    echo "已取消操作"
    exit 0
fi

echo ""
echo "开始清理..."

# 1. 备份 pip 包列表（如果有）
echo "[1/6] 备份 pip 包列表..."
if command -v pip3 &> /dev/null; then
    pip3 list --format=freeze > ~/python_packages_backup.txt 2>/dev/null || true
    echo "  ✓ 已备份到 ~/python_packages_backup.txt"
else
    echo "  - 未找到 pip3"
fi

# 2. 卸载 pyenv Python 版本
echo "[2/6] 卸载 pyenv Python 版本..."
if command -v pyenv &> /dev/null; then
    versions=$(pyenv versions --bare 2>/dev/null || true)
    if [ -n "$versions" ]; then
        echo "$versions" | while read -r version; do
            echo "  - 卸载 Python $version"
            pyenv uninstall -f "$version" 2>/dev/null || true
        done
        echo "  ✓ pyenv Python 版本已卸载"
    else
        echo "  - 未找到 pyenv Python 版本"
    fi
else
    echo "  - pyenv 未安装"
fi

# 3. 卸载 Homebrew Python
echo "[3/6] 卸载 Homebrew Python..."
if command -v brew &> /dev/null; then
    python_packages=$(brew list --formula 2>/dev/null | grep -i "^python@" || true)
    if [ -n "$python_packages" ]; then
        echo "$python_packages" | while read -r pkg; do
            echo "  - 卸载 $pkg"
            brew uninstall --ignore-dependencies "$pkg" 2>/dev/null || true
        done
        brew cleanup -s python@* 2>/dev/null || true
        echo "  ✓ Homebrew Python 已卸载"
    else
        echo "  - 未找到 Homebrew Python 包"
    fi
else
    echo "  - Homebrew 未安装"
fi

# 4. 清理 pip 缓存
echo "[4/6] 清理 pip 缓存..."
if command -v pip3 &> /dev/null; then
    pip3 cache purge 2>/dev/null || true
    echo "  ✓ pip 缓存已清理"
else
    echo "  - 未找到 pip3"
fi

# 5. 清理虚拟环境（仅显示，不自动删除）
echo "[5/6] 查找虚拟环境..."
venv_count=$(find ~ -maxdepth 3 -name ".venv" -type d 2>/dev/null | wc -l | tr -d ' ')
if [ "$venv_count" -gt 0 ]; then
    echo "  找到 $venv_count 个 .venv 目录"
    echo "  手动清理: find ~ -name '.venv' -type d -exec rm -rf {} +"
else
    echo "  - 未找到虚拟环境"
fi

# 6. 清理 pyenv（可选）
echo "[6/6] pyenv 配置..."
if [ -d ~/.pyenv ]; then
    echo "  pyenv 目录: ~/.pyenv"
    echo "  如需完全删除 pyenv:"
    echo "    rm -rf ~/.pyenv"
    echo "  然后编辑 ~/.zshrc，删除 pyenv 相关配置"
else
    echo "  - pyenv 目录不存在"
fi

echo ""
echo "=========================================="
echo "清理完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "  1. 安装 UV:"
echo "     curl -LsSf https://astral.sh/uv/install.sh | sh"
echo ""
echo "  2. 重新加载 shell:"
echo "     source ~/.zshrc"
echo ""
echo "  3. 安装 Python 3.11:"
echo "     uv python install 3.11"
echo ""
echo "  4. 进入项目并同步:"
echo "     cd /Users/apri/Documents/selfSync"
echo "     uv sync"
echo ""

