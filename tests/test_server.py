"""Tests for Ketcher MCP Server."""

import pytest

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False


@pytest.mark.skipif(not RDKIT_AVAILABLE, reason="RDKit not installed")
def test_rdkit_smiles_validation():
    """Test SMILES validation with RDKit."""
    # Valid SMILES
    mol = Chem.MolFromSmiles("CCO")
    assert mol is not None

    # Invalid SMILES
    mol = Chem.MolFromSmiles("INVALID")
    assert mol is None


@pytest.mark.skipif(not RDKIT_AVAILABLE, reason="RDKit not installed")
def test_rdkit_smiles_to_mol():
    """Test SMILES to MOL conversion."""
    mol = Chem.MolFromSmiles("CCO")
    assert mol is not None
    mol_block = Chem.MolToMolBlock(mol)
    assert "V2000" in mol_block or "V3000" in mol_block


@pytest.mark.skipif(not RDKIT_AVAILABLE, reason="RDKit not installed")
def test_rdkit_mol_to_smiles():
    """Test MOL to SMILES conversion."""
    mol = Chem.MolFromSmiles("CCO")
    mol_block = Chem.MolToMolBlock(mol)
    mol2 = Chem.MolFromMolBlock(mol_block)
    smiles = Chem.MolToSmiles(mol2)
    assert smiles == "CCO"


@pytest.mark.skipif(not RDKIT_AVAILABLE, reason="RDKit not installed")
def test_rdkit_molecule_properties():
    """Test molecular property calculation."""
    mol = Chem.MolFromSmiles("CCO")
    assert mol is not None

    # Test basic properties (without explicit hydrogens)
    assert mol.GetNumAtoms() == 3  # C, C, O (without H)
    assert Descriptors.MolWt(mol) > 0
    assert Descriptors.MolLogP(mol) is not None


@pytest.mark.skipif(not RDKIT_AVAILABLE, reason="RDKit not installed")
def test_rdkit_inchi_conversion():
    """Test SMILES to InChI conversion."""
    mol = Chem.MolFromSmiles("CCO")
    inchi = Chem.MolToInchi(mol)
    assert inchi.startswith("InChI=")


@pytest.mark.skipif(not RDKIT_AVAILABLE, reason="RDKit not installed")
def test_rdkit_inchikey_conversion():
    """Test SMILES to InChIKey conversion."""
    mol = Chem.MolFromSmiles("CCO")
    inchikey = Chem.MolToInchiKey(mol)
    assert len(inchikey) == 27
    assert "-" in inchikey


def test_ketcher_url():
    """Test Ketcher URL is defined."""
    from ketcher_mcp.server import KETCHER_URL
    assert KETCHER_URL.startswith("https://")
    assert "ketcher" in KETCHER_URL.lower()
