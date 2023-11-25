"""
Nimble RACCOON
F. Comitani     @2023-2024
"""

import toml
from pathlib import Path

from .raccoon import Raccoon

def get_version():
    pyproject_toml_path = Path(__file__).resolve()\
        .parent.parent.parent / "pyproject.toml"
    pyproject_toml = toml.load(pyproject_toml_path)
    
    return pyproject_toml["project"]["version"]

__version__ = get_version()