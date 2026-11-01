"""
folderforge

Create folders and files automatically from an AI-generated
text folder-tree structure.

Example:
    import folderforge
    folderforge.build("structure.txt")

"""

from .builder import build, build_from_text

__version__ = "1.0.0"
__all__ = ["build", "build_from_text"]