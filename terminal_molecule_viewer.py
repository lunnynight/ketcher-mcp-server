#!/usr/bin/env python3
"""
终端分子结构查看器
支持多种显示方式：
1. iTerm2 图像显示（推荐）
2. ASCII 艺术风格
3. 保存为图片并自动打开
"""

import argparse
import base64
import io
import os
import subprocess
import sys
from pathlib import Path

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw, Descriptors
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False
    print("❌ RDKit 未安装。请运行: pip install rdkit")
    sys.exit(1)


def display_iterm2(img_data: bytes):
    """在 iTerm2 中直接显示图片"""
    b64_data = base64.b64encode(img_data).decode()
    print(f"\033]1337;File=inline=1:{b64_data}\a")


def display_ascii(mol, width=80):
    """生成 ASCII 艺术风格的分子结构（简化版）"""
    smiles = Chem.MolToSmiles(mol)
    formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
    mw = Descriptors.MolWt(mol)

    # 简单的 ASCII 表示
    print("\n" + "=" * width)
    print(f"  分子式: {formula}")
    print(f"  分子量: {mw:.2f}")
    print(f"  SMILES: {smiles}")
    print("=" * width)

    # 显示原子和键的统计
    print(f"\n  原子数: {mol.GetNumAtoms()}")
    print(f"  键数: {mol.GetNumBonds()}")
    print(f"  环数: {Chem.rdMolDescriptors.CalcNumRings(mol)}")

    # 显示原子列表
    print("\n  原子列表:")
    atom_counts = {}
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        atom_counts[symbol] = atom_counts.get(symbol, 0) + 1

    for symbol, count in sorted(atom_counts.items()):
        print(f"    {symbol}: {count}")

    print()


def save_and_open(mol, output_path: str):
    """保存为图片并自动打开"""
    img = Draw.MolToImage(mol, size=(800, 600))
    img.save(output_path)
    print(f"✅ 图片已保存: {output_path}")

    # 自动打开图片
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", output_path])
    elif sys.platform == "linux":
        subprocess.run(["xdg-open", output_path])
    elif sys.platform == "win32":
        os.startfile(output_path)


def display_molecule(smiles: str, mode: str = "auto", output: str = None):
    """显示分子结构"""
    # 解析 SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"❌ 无效的 SMILES: {smiles}")
        return False

    print(f"\n🧪 分子: {smiles}")

    # 根据模式显示
    if mode == "ascii" or mode == "auto":
        display_ascii(mol)

    if mode == "iterm2":
        # 生成图片
        img = Draw.MolToImage(mol, size=(600, 400))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        display_iterm2(buffer.getvalue())

    if mode == "image" or output:
        output_path = output or f"molecule_{smiles[:20]}.png"
        save_and_open(mol, output_path)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="终端分子结构查看器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "CCO"                          # 乙醇（ASCII 模式）
  %(prog)s "CCO" -m iterm2                # iTerm2 图像显示
  %(prog)s "CCO" -m image                 # 保存并打开图片
  %(prog)s "CC(=O)Oc1ccccc1C(=O)O" -o aspirin.png  # 保存为指定文件

支持的显示模式:
  ascii   - ASCII 文本显示（默认）
  iterm2  - iTerm2 内联图像显示
  image   - 保存为图片并打开
  auto    - 自动选择（ASCII + 检测终端）
        """
    )

    parser.add_argument("smiles", help="SMILES 字符串")
    parser.add_argument(
        "-m", "--mode",
        choices=["ascii", "iterm2", "image", "auto"],
        default="auto",
        help="显示模式（默认: auto）"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出图片路径"
    )
    parser.add_argument(
        "-s", "--size",
        default="600x400",
        help="图片尺寸（默认: 600x400）"
    )

    args = parser.parse_args()

    # 显示分子
    success = display_molecule(args.smiles, args.mode, args.output)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
