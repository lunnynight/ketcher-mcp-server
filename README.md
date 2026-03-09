# Ketcher MCP Server

MCP (Model Context Protocol) server for Ketcher chemical structure editor integration with Claude.

## Features

- 🧪 **Open Ketcher Editor**: Launch Ketcher web interface in browser
- 🔄 **Format Conversion**: Convert between SMILES, MOL, InChI formats
- 🖼️ **Image Generation**: Generate PNG/SVG images from SMILES
- 📊 **Molecular Properties**: Calculate molecular weight, LogP, TPSA, etc.
- ✅ **Validation**: Validate SMILES strings

## Installation

### Prerequisites

- Python 3.10 or higher (tested with Python 3.11)
- pip

**Note**: If you're using macOS with system Python 3.9, you'll need to install Python 3.10+ separately:

```bash
# Using Homebrew
brew install python@3.11

# Verify installation
/opt/homebrew/bin/python3.11 --version
```

### Install Dependencies

```bash
cd ketcher-mcp-server

# If using Python 3.11 from Homebrew
/opt/homebrew/bin/python3.11 -m pip install -e .

# Or if python3 is already 3.10+
pip install -e .
```

### For Development

```bash
pip install -e ".[dev]"
```

## Usage

### Running the Server

```bash
python -m ketcher_mcp.server
```

Or use with `mcp` CLI:

```bash
mcp run ketcher_mcp.server
```

### Configuration for Claude Desktop

Add to your `claude_desktop_config.json`:

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

**Note**: Adjust the Python path based on your installation:
- Homebrew Python 3.11: `/opt/homebrew/bin/python3.11`
- System Python 3.10+: `python3` or `python3.10`
- Check your path with: `which python3.11`

On macOS, the config file is located at:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

## Available Tools

### 1. `open_ketcher`
Opens Ketcher chemical structure editor in your default web browser.

**Example:**
```
Open Ketcher editor
```

### 2. `smiles_to_image`
Converts SMILES notation to molecular structure image.

**Parameters:**
- `smiles` (str): SMILES notation
- `width` (int, optional): Image width (default: 400)
- `height` (int, optional): Image height (default: 300)
- `format` (str, optional): 'png' or 'svg' (default: 'png')

**Example:**
```
Generate image for aspirin: CC(=O)Oc1ccccc1C(=O)O
```

### 3. `smiles_to_mol`
Converts SMILES to MOL file format.

**Parameters:**
- `smiles` (str): SMILES notation

**Example:**
```
Convert CC(=O)Oc1ccccc1C(=O)O to MOL format
```

### 4. `mol_to_smiles`
Converts MOL file format to SMILES.

**Parameters:**
- `mol_block` (str): MOL file content

### 5. `get_molecule_properties`
Calculates molecular properties from SMILES.

**Parameters:**
- `smiles` (str): SMILES notation

**Returns:**
- Molecular formula
- Molecular weight
- Number of atoms, bonds, rings
- LogP, TPSA
- Hydrogen bond donors/acceptors
- Rotatable bonds

**Example:**
```
Get properties of caffeine: CN1C=NC2=C1C(=O)N(C(=O)N2C)C
```

### 6. `validate_smiles`
Validates a SMILES string.

**Parameters:**
- `smiles` (str): SMILES notation to validate

**Example:**
```
Validate SMILES: CCO
```

### 7. `smiles_to_inchi`
Converts SMILES to InChI identifier.

**Parameters:**
- `smiles` (str): SMILES notation

### 8. `smiles_to_inchikey`
Converts SMILES to InChIKey identifier.

**Parameters:**
- `smiles` (str): SMILES notation

## Example Workflows

### Workflow 1: Draw and Analyze a Molecule

1. "Open Ketcher editor"
2. Draw your molecule in Ketcher
3. Copy the SMILES from Ketcher
4. "Get properties of [SMILES]"
5. "Generate image for [SMILES]"

### Workflow 2: Convert Chemical Formats

1. "Convert aspirin SMILES to MOL format: CC(=O)Oc1ccccc1C(=O)O"
2. "Convert this MOL to InChI"
3. "Generate InChIKey"

### Workflow 3: Validate and Visualize

1. "Validate SMILES: CCO"
2. "Generate SVG image for CCO"
3. "Get molecular properties"

## Technical Details

### Architecture

- **FastMCP**: MCP server framework
- **RDKit**: Chemical informatics library for molecule processing
- **Ketcher**: Web-based chemical structure editor (via CDN)

### Supported Formats

- **SMILES**: Simplified Molecular Input Line Entry System
- **MOL**: MDL Molfile format
- **InChI**: IUPAC International Chemical Identifier
- **InChIKey**: Hashed InChI for database lookups
- **PNG/SVG**: Image formats for visualization

## Troubleshooting

### RDKit Installation Issues

If you encounter issues installing RDKit:

```bash
# Using conda (recommended)
conda install -c conda-forge rdkit

# Or using pip
pip install rdkit-pypi
```

### Ketcher Not Opening

Make sure you have a default web browser configured. The server uses Python's `webbrowser` module.

## Development

### Running Tests

```bash
pytest
```

### Project Structure

```
ketcher-mcp-server/
├── ketcher_mcp/
│   ├── __init__.py
│   └── server.py
├── pyproject.toml
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License

## Acknowledgments

- [Ketcher](https://github.com/epam/ketcher) - EPAM's open-source chemical structure editor
- [RDKit](https://www.rdkit.org/) - Open-source cheminformatics toolkit
- [FastMCP](https://github.com/jlowin/fastmcp) - Fast MCP server framework

## Version History

- **0.1.0** (2026-03-09): Initial release
  - Basic SMILES/MOL conversion
  - Image generation
  - Molecular property calculation
  - Ketcher integration
