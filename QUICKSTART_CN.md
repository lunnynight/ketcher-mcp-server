# 快速开始指南

## 安装步骤

### 1. 检查 Python 版本

```bash
python3 --version
```

如果版本低于 3.10，需要安装更高版本：

```bash
# macOS (使用 Homebrew)
brew install python@3.11

# 验证安装
/opt/homebrew/bin/python3.11 --version
```

### 2. 安装 Ketcher MCP 服务器

```bash
cd ~/ketcher-mcp-server

# 使用 Python 3.11
/opt/homebrew/bin/python3.11 -m pip install -e .
```

### 3. 配置 Claude Desktop

编辑配置文件：

```bash
# macOS
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 或使用命令行编辑器
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

添加以下内容：

```json
{
  "mcpServers": {
    "ketcher": {
      "command": "/opt/homebrew/bin/python3.11",
      "args": ["-m", "ketcher_mcp.server"]
    }
  }
}
```

### 4. 重启 Claude Desktop

完全退出并重新启动 Claude Desktop 应用。

### 5. 测试功能

在 Claude 中尝试以下命令：

```
打开 Ketcher 编辑器
```

```
生成阿司匹林的分子结构图：CC(=O)Oc1ccccc1C(=O)O
```

```
获取咖啡因的分子属性：CN1C=NC2=C1C(=O)N(C(=O)N2C)C
```

## 常用功能

### 1. 打开 Ketcher 编辑器

```
打开 Ketcher
```

这会在浏览器中打开 Ketcher 化学结构编辑器。

### 2. 生成分子图像

```
生成乙醇的分子结构图：CCO
```

### 3. 获取分子属性

```
获取阿司匹林的分子属性：CC(=O)Oc1ccccc1C(=O)O
```

返回信息包括：
- 分子式
- 分子量
- LogP（脂水分配系数）
- TPSA（拓扑极性表面积）
- 氢键供体/受体数量
- 可旋转键数量

### 4. 格式转换

```
将 SMILES 转换为 MOL 格式：CCO
```

```
将 SMILES 转换为 InChI：CCO
```

### 5. 验证 SMILES

```
验证 SMILES 字符串：CCO
```

## 常见问题

### Q: 提示 "RDKit is not installed"

A: 重新安装依赖：

```bash
/opt/homebrew/bin/python3.11 -m pip install rdkit
```

### Q: Claude Desktop 找不到 MCP 服务器

A: 检查以下几点：
1. Python 路径是否正确（使用 `which python3.11` 查看）
2. 是否完全重启了 Claude Desktop
3. 配置文件 JSON 格式是否正确

### Q: 如何查看 MCP 服务器日志

A: 在终端中直接运行服务器：

```bash
/opt/homebrew/bin/python3.11 -m ketcher_mcp.server
```

## 示例工作流

### 工作流 1：绘制并分析分子

1. "打开 Ketcher 编辑器"
2. 在 Ketcher 中绘制分子结构
3. 复制 SMILES 字符串
4. "获取这个分子的属性：[粘贴 SMILES]"
5. "生成这个分子的图像：[粘贴 SMILES]"

### 工作流 2：化学格式转换

1. "将阿司匹林 SMILES 转换为 MOL 格式：CC(=O)Oc1ccccc1C(=O)O"
2. "转换为 InChI 格式"
3. "生成 InChIKey"

### 工作流 3：批量验证

1. "验证 SMILES：CCO"
2. "验证 SMILES：CC(=O)Oc1ccccc1C(=O)O"
3. "验证 SMILES：CN1C=NC2=C1C(=O)N(C(=O)N2C)C"

## 支持的化学格式

- **SMILES**: 简化分子线性输入规范
- **MOL**: MDL Molfile 格式
- **InChI**: IUPAC 国际化学标识符
- **InChIKey**: InChI 的哈希版本
- **PNG/SVG**: 图像格式

## 下一步

- 查看完整文档：[README.md](README.md)
- 运行测试：`/opt/homebrew/bin/python3.11 -m pytest tests/`
- 贡献代码：提交 Issue 或 Pull Request
