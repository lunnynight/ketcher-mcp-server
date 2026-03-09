#!/bin/bash
# Ketcher MCP Server 自动配置脚本

set -e

echo "🧪 Ketcher MCP Server 自动配置"
echo "================================"

# 检测 Python 3.10+
PYTHON_CMD=""
for cmd in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON_CMD=$(which $cmd)
            echo "✅ 找到 Python $VERSION: $PYTHON_CMD"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ 错误：需要 Python 3.10 或更高版本"
    echo "请先安装：brew install python@3.11"
    exit 1
fi

# Claude Desktop 配置文件路径
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# 备份现有配置
if [ -f "$CONFIG_FILE" ]; then
    echo "📦 备份现有配置..."
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 创建配置目录
mkdir -p "$(dirname "$CONFIG_FILE")"

# 读取现有配置或创建新配置
if [ -f "$CONFIG_FILE" ]; then
    # 使用 Python 合并配置
    $PYTHON_CMD << EOF
import json
import sys

config_file = "$CONFIG_FILE"
python_cmd = "$PYTHON_CMD"

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    config = {}

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['ketcher'] = {
    'command': python_cmd,
    'args': ['-m', 'ketcher_mcp.server']
}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 配置已更新")
EOF
else
    # 创建新配置
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "ketcher": {
      "command": "$PYTHON_CMD",
      "args": ["-m", "ketcher_mcp.server"]
    }
  }
}
EOF
    echo "✅ 配置文件已创建"
fi

echo ""
echo "🎉 配置完成！"
echo ""
echo "下一步："
echo "1. 完全退出 Claude Desktop（Cmd+Q）"
echo "2. 重新启动 Claude Desktop"
echo "3. 在对话中输入：打开 Ketcher"
echo ""
echo "如需恢复配置，备份文件位于："
echo "   $CONFIG_FILE.backup.*"
