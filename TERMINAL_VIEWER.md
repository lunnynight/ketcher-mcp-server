# 终端分子查看器 (Molecule Terminal Viewer)

在终端中直接查看和分析分子结构的强大工具。

## 功能特性

- 🎨 **ASCII 艺术显示** - 在终端中以 ASCII 艺术形式显示分子结构
- 📊 **详细信息** - 显示分子式、分子量、LogP、TPSA 等属性
- 🖼️ **iTerm2 集成** - 在 iTerm2 中直接显示高清图像
- 💾 **图片导出** - 保存为 PNG 格式并自动打开
- ⚡ **快速便捷** - 命令行工具，无需打开浏览器

## 安装

```bash
# 已包含在 ketcher-mcp-server 项目中
cd ~/ketcher-mcp-server

# 确保依赖已安装
/opt/homebrew/bin/python3.11 -m pip install rdkit pillow

# 添加到 PATH（可选）
ln -s ~/ketcher-mcp-server/molview /usr/local/bin/molview
```

## 使用方法

### 基本用法

```bash
# 显示 ASCII 艺术（默认）
./molview "CCO"

# 显示详细信息
./molview "CCO" -m info

# 显示所有信息（信息 + ASCII 艺术）
./molview "CCO" -m all

# 在 iTerm2 中显示图像
./molview "CCO" -m iterm2

# 保存为图片
./molview "CCO" -m image -o ethanol.png
```

### 常用分子示例

```bash
# 乙醇
./molview "CCO" -m all

# 阿司匹林
./molview "CC(=O)Oc1ccccc1C(=O)O" -m all -w 120

# 咖啡因
./molview "CN1C=NC2=C1C(=O)N(C(=O)N2C)C" -m all

# 青霉素
./molview "CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O" -m all

# 葡萄糖
./molview "C(C1C(C(C(C(O1)O)O)O)O)O" -m all
```

## 显示模式

### 1. info - 详细信息模式

显示分子的详细属性：

```bash
./molview "CCO" -m info
```

输出：
```
================================================================================
  🧪 分子信息
================================================================================
  SMILES:     CCO
  规范SMILES: CCO
  分子式:     C2H6O
  分子量:     46.07 g/mol
  LogP:       -0.03
  TPSA:       20.23 Ų
  原子数:     3
  重原子数:   3
  键数:       2
  环数:       0
  芳香环数:   0
  氢键供体:   1
  氢键受体:   1
  可旋转键:   0
================================================================================
```

### 2. ascii - ASCII 艺术模式

以 ASCII 艺术形式显示分子结构：

```bash
./molview "CCO" -m ascii -w 100
```

参数：
- `-w, --width`: ASCII 艺术宽度（默认 80）
- `--invert`: 反转颜色（白色背景）

### 3. iterm2 - iTerm2 图像模式

在 iTerm2 终端中直接显示高清图像：

```bash
./molview "CCO" -m iterm2
```

**注意**: 仅支持 iTerm2 终端

### 4. image - 图片保存模式

保存为 PNG 图片并自动打开：

```bash
./molview "CCO" -m image -o ethanol.png
```

参数：
- `-o, --output`: 输出文件路径
- `--no-open`: 保存后不自动打开

### 5. all - 完整模式

显示所有信息（详细信息 + ASCII 艺术）：

```bash
./molview "CCO" -m all -w 120
```

## 高级用法

### 批量处理

```bash
# 处理多个分子
for smiles in "CCO" "CC(=O)Oc1ccccc1C(=O)O" "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"; do
    echo "处理: $smiles"
    ./molview "$smiles" -m info
    echo "---"
done
```

### 管道处理

```bash
# 从文件读取 SMILES
cat molecules.txt | while read smiles; do
    ./molview "$smiles" -m ascii
done
```

### 生成报告

```bash
# 生成 HTML 报告
./molview "CCO" -m info > ethanol_report.txt
./molview "CCO" -m image -o ethanol.png --no-open
```

## 命令行参数

```
usage: molview [-h] [-m {info,ascii,iterm2,image,all}] [-w WIDTH] [-o OUTPUT]
               [--no-open] [--invert]
               smiles

Molecule Terminal Viewer - 终端分子查看器

positional arguments:
  smiles                SMILES 字符串

options:
  -h, --help            显示帮助信息
  -m, --mode {info,ascii,iterm2,image,all}
                        显示模式（默认: ascii）
  -w, --width WIDTH     ASCII 艺术宽度（默认: 80）
  -o, --output OUTPUT   输出图片路径
  --no-open             保存图片后不自动打开
  --invert              反转 ASCII 艺术颜色
```

## 与 MCP 集成

Ketcher MCP Server 已集成终端查看功能，可以在 Claude 中直接使用：

```
在终端显示乙醇的分子结构：CCO
```

Claude 会自动调用 `molview` 工具生成 ASCII 艺术。

## 技术细节

### 依赖库

- **RDKit**: 化学信息学库，用于分子处理
- **Pillow**: 图像处理库，用于 ASCII 艺术转换

### ASCII 艺术算法

1. 使用 RDKit 生成分子的 2D 图像
2. 将图像转换为灰度
3. 调整图像大小以适应终端宽度
4. 将每个像素映射到 ASCII 字符集：`@%#*+=-:. `
5. 输出 ASCII 艺术

### iTerm2 图像协议

使用 iTerm2 的内联图像协议（Inline Images Protocol）：

```
\033]1337;File=inline=1:<base64_data>\a
```

## 常见问题

### Q: ASCII 艺术显示不清晰

A: 尝试增加宽度参数：

```bash
./molview "CCO" -m ascii -w 120
```

### Q: iTerm2 模式不工作

A: 确保你使用的是 iTerm2 终端，其他终端不支持此功能。

### Q: 图片无法自动打开

A: 使用 `--no-open` 参数手动打开：

```bash
./molview "CCO" -m image -o ethanol.png --no-open
open ethanol.png
```

### Q: RDKit 导入错误

A: 重新安装 RDKit：

```bash
/opt/homebrew/bin/python3.11 -m pip install --upgrade rdkit
```

## 示例输出

### 咖啡因（Caffeine）

```bash
./molview "CN1C=NC2=C1C(=O)N(C(=O)N2C)C" -m all -w 100
```

输出：
```
================================================================================
  🧪 分子信息
================================================================================
  SMILES:     CN1C=NC2=C1C(=O)N(C(=O)N2C)C
  规范SMILES: Cn1c(=O)c2c(ncn2C)n(C)c1=O
  分子式:     C8H10N4O2
  分子量:     194.19 g/mol
  LogP:       -1.03
  TPSA:       61.82 Ų
  原子数:     14
  重原子数:   14
  键数:       15
  环数:       2
  芳香环数:   2
  氢键供体:   0
  氢键受体:   3
  可旋转键:   0
================================================================================

[ASCII 艺术显示咖啡因分子结构]
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 相关项目

- [Ketcher MCP Server](./README.md) - MCP 服务器
- [RDKit](https://www.rdkit.org/) - 化学信息学工具包
- [rdkit-cli](https://github.com/Vitruves/rdkit-cli) - RDKit 命令行工具
