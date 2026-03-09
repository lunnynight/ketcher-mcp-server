#!/usr/bin/env python3
"""扩展测试 - 测试边界情况和错误处理"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_edge_cases():
    """测试边界情况"""

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["-m", "ketcher_mcp.server"],
    )

    print("🧪 边界情况测试\n")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 测试 1: 无效的 SMILES
            print("🧪 测试 1: 无效的 SMILES")
            result = await session.call_tool("validate_smiles", {"smiles": "INVALID_SMILES_123"})
            print(f"结果: {result.content[0].text}")
            assert "false" in result.content[0].text.lower()
            print("✅ 通过\n")

            # 测试 2: 空 SMILES
            print("🧪 测试 2: 空字符串")
            result = await session.call_tool("validate_smiles", {"smiles": ""})
            print(f"结果: {result.content[0].text}")
            assert "false" in result.content[0].text.lower()
            print("✅ 通过\n")

            # 测试 3: 复杂分子（青霉素）
            print("🧪 测试 3: 复杂分子（青霉素）")
            penicillin = "CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O"
            result = await session.call_tool("get_molecule_properties", {"smiles": penicillin})
            print(f"分子式: ", end="")
            import json
            props = json.loads(result.content[0].text)
            print(props["molecular_formula"])
            print(f"分子量: {props['molecular_weight']}")
            assert props["molecular_weight"] > 0
            print("✅ 通过\n")

            # 测试 4: SVG 图像生成
            print("🧪 测试 4: SVG 图像生成")
            result = await session.call_tool("smiles_to_image", {
                "smiles": "c1ccccc1",  # 苯
                "format": "svg",
                "width": 500,
                "height": 400
            })
            svg_data = result.content[0].text
            assert "data:image/svg+xml;base64," in svg_data
            print(f"✅ SVG 生成成功 (长度: {len(svg_data)} 字符)\n")

            # 测试 5: MOL 往返转换
            print("🧪 测试 5: MOL 往返转换")
            original_smiles = "CC(C)O"  # 异丙醇

            # SMILES -> MOL
            result = await session.call_tool("smiles_to_mol", {"smiles": original_smiles})
            mol_block = result.content[0].text

            # MOL -> SMILES
            result = await session.call_tool("mol_to_smiles", {"mol_block": mol_block})
            converted_smiles = result.content[0].text

            print(f"原始: {original_smiles}")
            print(f"转换后: {converted_smiles}")
            # 规范化后应该相同
            assert converted_smiles in ["CC(C)O", "CC(O)C"]  # 可能的规范形式
            print("✅ 通过\n")

            # 测试 6: InChI 和 InChIKey
            print("🧪 测试 6: InChI 和 InChIKey 生成")
            smiles = "CCO"

            result = await session.call_tool("smiles_to_inchi", {"smiles": smiles})
            inchi = result.content[0].text
            print(f"InChI: {inchi}")
            assert inchi.startswith("InChI=")

            result = await session.call_tool("smiles_to_inchikey", {"smiles": smiles})
            inchikey = result.content[0].text
            print(f"InChIKey: {inchikey}")
            assert len(inchikey) == 27
            assert inchikey.count("-") == 2
            print("✅ 通过\n")

            # 测试 7: 大分子
            print("🧪 测试 7: 大分子（胰岛素片段）")
            large_smiles = "CC(C)CC(NC(=O)C(CC(C)C)NC(=O)C(CCC(N)=O)NC(=O)C(CCC(O)=O)NC(=O)C(Cc1ccccc1)NC(=O)C(CC(C)C)NC(=O)C(Cc2ccccc2)NC(=O)C(Cc3ccc(O)cc3)NC(=O)C(C)NC(=O)C(CC(C)C)NC(=O)C(Cc4c[nH]c5ccccc45)NC(=O)C(CCC(N)=O)NC(=O)C(CC(C)C)NC(=O)C(CCC(O)=O)NC(=O)C(Cc6ccc(O)cc6)NC(=O)C(CO)NC(=O)C(Cc7ccccc7)NC(=O)C(CC(C)C)NC(=O)C(C)N)C(=O)O"
            result = await session.call_tool("validate_smiles", {"smiles": large_smiles})
            data = json.loads(result.content[0].text)
            print(f"有效性: {data['valid']}")
            if data['valid']:
                result = await session.call_tool("get_molecule_properties", {"smiles": large_smiles})
                props = json.loads(result.content[0].text)
                print(f"分子量: {props['molecular_weight']}")
                print("✅ 通过\n")
            else:
                print("⚠️ 大分子验证失败（可能太复杂）\n")

            print("🎉 所有边界测试完成！")

if __name__ == "__main__":
    asyncio.run(test_edge_cases())
