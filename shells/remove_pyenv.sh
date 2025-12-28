#!/bin/bash
# 彻底移除 pyenv 脚本

set -e

echo "=========================================="
echo "彻底移除 pyenv"
echo "=========================================="
echo ""

# 1. 卸载 Homebrew 的 pyenv
echo "[1/5] 检查并卸载 Homebrew pyenv..."
if brew list --formula 2>/dev/null | grep -q "^pyenv$"; then
    echo "  发现 Homebrew 安装的 pyenv，正在卸载..."
    brew uninstall pyenv
    echo "  ✓ 已卸载"
else
    echo "  ✓ Homebrew pyenv 未安装"
fi

# 2. 删除 pyenv 目录
echo "[2/5] 删除 ~/.pyenv 目录..."
if [ -d ~/.pyenv ]; then
    rm -rf ~/.pyenv
    echo "  ✓ 已删除 ~/.pyenv"
else
    echo "  ✓ ~/.pyenv 目录不存在"
fi

# 3. 清理配置文件中的 pyenv 行
echo "[3/5] 清理配置文件中的 pyenv 配置..."
for file in ~/.zshrc ~/.zprofile ~/.zshenv ~/.bash_profile ~/.bashrc; do
    if [ -f "$file" ]; then
        # 备份
        if ! grep -q "pyenv" "$file"; then
            echo "  - $file: 无 pyenv 配置"
        else
            # 创建备份
            cp "$file" "${file}.backup-$(date +%Y%m%d-%H%M%S)" 2>/dev/null || true
            # 删除包含 pyenv 的行（包括注释）
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' '/pyenv/d' "$file" 2>/dev/null || true
            else
                # Linux
                sed -i '/pyenv/d' "$file" 2>/dev/null || true
            fi
            echo "  ✓ 已清理 $file"
        fi
    fi
done

# 4. 清理当前会话的 pyenv 函数（临时）
echo "[4/5] 清理当前 shell 会话中的 pyenv..."
if type pyenv &>/dev/null; then
    unset -f pyenv 2>/dev/null || true
    # 从 PATH 中移除 pyenv shims
    export PATH=$(echo $PATH | tr ':' '\n' | grep -v pyenv | tr '\n' ':' | sed 's/:$//')
    echo "  ✓ 已从当前会话移除 pyenv（临时）"
else
    echo "  ✓ 当前会话中无 pyenv 函数"
fi

# 5. 验证和提示
echo "[5/5] 验证..."
echo ""
echo "=========================================="
echo "清理完成！"
echo "=========================================="
echo ""
echo "⚠️  重要：请执行以下操作："
echo ""
echo "1. 关闭当前终端并打开新终端（必需！）"
echo ""
echo "2. 在新终端中验证："
echo "   which pyenv      # 应该显示: pyenv not found"
echo "   type pyenv       # 应该显示: pyenv: not found"
echo "   pyenv --version  # 应该显示: command not found"
echo ""
echo "3. 如果验证通过，安装 UV："
echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
echo "   source ~/.zshrc"
echo ""
echo "4. 安装 Python："
echo "   uv python install 3.11"
echo ""

