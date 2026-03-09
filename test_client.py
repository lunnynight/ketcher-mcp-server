#!/usr/bin/env python3
"""简单的 MCP 客户端，用于测试 Ketcher MCP 服务器"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_ketcher_mcp():
    """测试 Ketcher MCP 服务器的所有功能"""

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["-m", "ketcher_mcp.server"],
    )

    print("🧪 连接到 Ketcher MCP 服务器...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("✅ 连接成功！\n")

            # 列出所有工具
            tools = await session.list_tools()
            print(f"📋 可用工具 ({len(tools.tools)} 个):")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()

            # 测试 1: 验证 SMILES
            print("🧪 测试 1: 验证 SMILES (乙醇: CCO)")
            result = await session.call_tool("validate_smiles", {"smiles": "CCO"})
            print(f"结果: {result.content[0].text}\n")

            # 测试 2: 获取分子属性
            print("🧪 测试 2: 获取分子属性 (阿司匹林)")
            aspirin = "CC(=O)Oc1ccccc1C(=O)O"
            result = await session.call_tool("get_molecule_properties", {"smiles": aspirin})
            print(f"结果:\n{result.content[0].text}\n")

            # 测试 3: SMILES 转 MOL
            print("🧪 测试 3: SMILES 转 MOL (乙醇)")
            result = await session.call_tool("smiles_to_mol", {"smiles": "CCO"})
            mol_text = result.content[0].text
            print(f"MOL 文件 (前 5 行):")
            for line in mol_text.split('\n')[:5]:
                print(f"  {line}")
            print()

            # 测试 4: SMILES 转 InChI
            print("🧪 测试 4: SMILES 转 InChI (咖啡因)")
            caffeine = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
            result = await session.call_tool("smiles_to_inchi", {"smiles": caffeine})
            print(f"InChI: {result.content[0].text}\n")

            # 测试 5: 生成图像
            print("🧪 测试 5: 生成分子图像 (乙醇)")
            result = await session.call_tool("smiles_to_image", {
                "smiles": "CCO",
                "width": 300,
                "height": 200,
                "format": "png"
            })
            img_data = result.content[0].text
            if img_data.startswith("data:image/png;base64,"):
                print(f"✅ 图像生成成功 (Base64 长度: {len(img_data)} 字符)\n")
            else:
                print(f"❌ 图像生成失败\n")

            print("🎉 所有测试完成！")

if __name__ == "__main__":
    asyncio.run(test_ketcher_mcp())
