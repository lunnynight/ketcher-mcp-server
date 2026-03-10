#!/usr/bin/env python3
"""
高级分子 ASCII 艺术生成器
使用图像转 ASCII 技术生成分子结构的 ASCII 艺术
"""

import argparse
import io
import sys

try:
    from rdkit import Chem
    from rdkit.Chem import Draw
    from PIL import Image
    RDKIT_AVAILABLE = True
except ImportError:
    print("❌ 需要安装: pip install rdkit pillow")
    sys.exit(1)


# ASCII 字符集（从暗到亮）
ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image, width=100):
    """将图像转换为 ASCII 艺术"""
    # 调整图像大小
    aspect_ratio = image.height / image.width
    new_height = int(width * aspect_ratio * 0.55)  # 0.55 调整字符宽高比
    image = image.resize((width, new_height))

    # 转换为灰度
    image = image.convert("L")

    # 转换为 ASCII
    pixels = image.getdata()
    ascii_str = ""

    for i, pixel in enumerate(pixels):
        # 反转亮度（黑色背景）
        pixel = 255 - pixel
        ascii_str += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]

        if (i + 1) % width == 0:
            ascii_str += "\n"

    return ascii_str


def molecule_to_ascii(smiles, width=80, invert=False):
    """将 SMILES 转换为 ASCII 艺术"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # 生成分子图像
    img = Draw.MolToImage(mol, size=(800, 600))

    # 如果需要反转颜色（白色背景）
    if invert:
        img = Image.eval(img, lambda x: 255 - x)

    # 转换为 ASCII
    ascii_art = image_to_ascii(img, width)

    return ascii_art


def main():
    parser = argparse.ArgumentParser(
        description="分子 ASCII 艺术生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "CCO"                          # 乙醇
  %(prog)s "CCO" -w 120                   # 更宽的显示
  %(prog)s "CC(=O)Oc1ccccc1C(=O)O"        # 阿司匹林
  %(prog)s "CN1C=NC2=C1C(=O)N(C(=O)N2C)C" # 咖啡因
        """
    )

    parser.add_argument("smiles", help="SMILES 字符串")
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=80,
        help="ASCII 艺术宽度（默认: 80）"
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="反转颜色（白色背景）"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="显示分子信息"
    )

    args = parser.parse_args()

    # 显示分子信息
    if args.info:
        mol = Chem.MolFromSmiles(args.smiles)
        if mol:
            from rdkit.Chem import Descriptors, rdMolDescriptors
            print(f"\n🧪 分子信息:")
            print(f"  SMILES: {args.smiles}")
            print(f"  分子式: {rdMolDescriptors.CalcMolFormula(mol)}")
            print(f"  分子量: {Descriptors.MolWt(mol):.2f}")
            print(f"  原子数: {mol.GetNumAtoms()}")
            print(f"  键数: {mol.GetNumBonds()}")
            print()

    # 生成 ASCII 艺术
    ascii_art = molecule_to_ascii(args.smiles, args.width, args.invert)

    if ascii_art:
        print(ascii_art)
    else:
        print(f"❌ 无效的 SMILES: {args.smiles}")
        sys.exit(1)


if __name__ == "__main__":
    main()
