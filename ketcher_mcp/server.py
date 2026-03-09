"""Ketcher MCP Server implementation using standard MCP SDK."""

import asyncio
import base64
import io
import json
import webbrowser
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, Draw
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False

# Ketcher standalone URL (using official CDN)
KETCHER_URL = "https://lifescience.opensource.epam.com/ketcher/index.html"

# Initialize MCP server
server = Server("ketcher")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="open_ketcher",
            description="Open Ketcher chemical structure editor in the default web browser",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="smiles_to_image",
            description="Convert SMILES string to molecular structure image (PNG or SVG)",
            inputSchema={
                "type": "object",
                "properties": {
                    "smiles": {"type": "string", "description": "SMILES notation of the molecule"},
                    "width": {"type": "integer", "description": "Image width in pixels", "default": 400},
                    "height": {"type": "integer", "description": "Image height in pixels", "default": 300},
                    "format": {"type": "string", "enum": ["png", "svg"], "description": "Output format", "default": "png"},
                },
                "required": ["smiles"],
            },
        ),
        Tool(
            name="smiles_to_mol",
            description="Convert SMILES string to MOL file format",
            inputSchema={
                "type": "object",
                "properties": {
                    "smiles": {"type": "string", "description": "SMILES notation of the molecule"},
                },
                "required": ["smiles"],
            },
        ),
        Tool(
            name="mol_to_smiles",
            description="Convert MOL file format to SMILES string",
            inputSchema={
                "type": "object",
                "properties": {
                    "mol_block": {"type": "string", "description": "MOL file content"},
                },
                "required": ["mol_block"],
            },
        ),
        Tool(
            name="get_molecule_properties",
            description="Get molecular properties from SMILES (formula, weight, LogP, TPSA, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "smiles": {"type": "string", "description": "SMILES notation of the molecule"},
                },
                "required": ["smiles"],
            },
        ),
        Tool(
            name="validate_smiles",
            description="Validate a SMILES string",
            inputSchema={
                "type": "object",
                "properties": {
                    "smiles": {"type": "string", "description": "SMILES notation to validate"},
                },
                "required": ["smiles"],
            },
        ),
        Tool(
            name="smiles_to_inchi",
            description="Convert SMILES to InChI identifier",
            inputSchema={
                "type": "object",
                "properties": {
                    "smiles": {"type": "string", "description": "SMILES notation of the molecule"},
                },
                "required": ["smiles"],
            },
        ),
        Tool(
            name="smiles_to_inchikey",
            description="Convert SMILES to InChIKey identifier",
            inputSchema={
                "type": "object",
                "properties": {
                    "smiles": {"type": "string", "description": "SMILES notation of the molecule"},
                },
                "required": ["smiles"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if not RDKIT_AVAILABLE and name != "open_ketcher":
        return [TextContent(
            type="text",
            text="Error: RDKit is not installed. Please install it with: pip install rdkit"
        )]

    if name == "open_ketcher":
        webbrowser.open(KETCHER_URL)
        return [TextContent(
            type="text",
            text=f"Ketcher editor opened in browser: {KETCHER_URL}"
        )]

    elif name == "smiles_to_image":
        smiles = arguments["smiles"]
        width = arguments.get("width", 400)
        height = arguments.get("height", 300)
        format_type = arguments.get("format", "png").lower()

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return [TextContent(type="text", text=f"Error: Invalid SMILES string: {smiles}")]

        if format_type == "svg":
            drawer = Draw.rdMolDraw2D.MolDraw2DSVG(width, height)
            drawer.DrawMolecule(mol)
            drawer.FinishDrawing()
            svg_data = drawer.GetDrawingText()
            svg_b64 = base64.b64encode(svg_data.encode()).decode()
            result = f"data:image/svg+xml;base64,{svg_b64}"
        else:
            img = Draw.MolToImage(mol, size=(width, height))
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode()
            result = f"data:image/png;base64,{img_b64}"

        return [TextContent(type="text", text=result)]

    elif name == "smiles_to_mol":
        smiles = arguments["smiles"]
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return [TextContent(type="text", text=f"Error: Invalid SMILES string: {smiles}")]

        AllChem.Compute2DCoords(mol)
        mol_block = Chem.MolToMolBlock(mol)
        return [TextContent(type="text", text=mol_block)]

    elif name == "mol_to_smiles":
        mol_block = arguments["mol_block"]
        mol = Chem.MolFromMolBlock(mol_block)
        if mol is None:
            return [TextContent(type="text", text="Error: Invalid MOL block")]

        smiles = Chem.MolToSmiles(mol)
        return [TextContent(type="text", text=smiles)]

    elif name == "get_molecule_properties":
        smiles = arguments["smiles"]
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return [TextContent(type="text", text=f"Error: Invalid SMILES string: {smiles}")]

        props = {
            "smiles": smiles,
            "molecular_formula": Chem.rdMolDescriptors.CalcMolFormula(mol),
            "molecular_weight": round(Descriptors.MolWt(mol), 2),
            "num_atoms": mol.GetNumAtoms(),
            "num_heavy_atoms": mol.GetNumHeavyAtoms(),
            "num_bonds": mol.GetNumBonds(),
            "num_rings": Chem.rdMolDescriptors.CalcNumRings(mol),
            "num_aromatic_rings": Chem.rdMolDescriptors.CalcNumAromaticRings(mol),
            "logp": round(Descriptors.MolLogP(mol), 2),
            "tpsa": round(Descriptors.TPSA(mol), 2),
            "num_hbd": Descriptors.NumHDonors(mol),
            "num_hba": Descriptors.NumHAcceptors(mol),
            "num_rotatable_bonds": Descriptors.NumRotatableBonds(mol),
        }
        return [TextContent(type="text", text=json.dumps(props, indent=2))]

    elif name == "validate_smiles":
        smiles = arguments["smiles"]
        # Check for empty string
        if not smiles or not smiles.strip():
            result = {"valid": False, "error": "Empty SMILES string"}
        else:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                result = {"valid": False, "error": "Invalid SMILES syntax"}
            else:
                result = {"valid": True, "canonical_smiles": Chem.MolToSmiles(mol)}
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "smiles_to_inchi":
        smiles = arguments["smiles"]
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return [TextContent(type="text", text=f"Error: Invalid SMILES string: {smiles}")]

        inchi = Chem.MolToInchi(mol)
        return [TextContent(type="text", text=inchi)]

    elif name == "smiles_to_inchikey":
        smiles = arguments["smiles"]
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return [TextContent(type="text", text=f"Error: Invalid SMILES string: {smiles}")]

        inchikey = Chem.MolToInchiKey(mol)
        return [TextContent(type="text", text=inchikey)]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
