import re
from dataclasses import dataclass, field
from pathlib import PureWindowsPath, PurePosixPath


TREE_NAME_PATTERN = re.compile(r"(?:├──|└──|--)\s*(.+)$")
CLEAN_NAME_PATTERN = re.compile(r"[\u2500-\u257F│├└─]")


@dataclass
class Node:
    name: str
    depth: int
    parent: str | None = None
    is_folder: bool = False
    children: list["Node"] = field(default_factory=list)


def _get_indent_depth(prefix: str) -> int:
    """
    Calculates nesting depth from the space before a file/folder name.

    Examples:
        "│   "       -> depth 1
        "│   ├── "   -> depth 1
        "│   │   "   -> depth 2
    """
    cleaned = CLEAN_NAME_PATTERN.sub(" ", prefix)
    cleaned = cleaned.replace("\t", "    ")

    leading_spaces = len(cleaned) - len(cleaned.lstrip(" "))
    return leading_spaces // 4


def _extract_name(line: str) -> tuple[str, int]:
    """
    Returns (name, depth) from one tree line.
    """
    match = TREE_NAME_PATTERN.search(line)

    if match:
        name = match.group(1).strip()
        prefix = line[: match.start()]
    else:
        name = line.strip()
        prefix = ""

    if not name:
        raise ValueError(f"Could not find a folder or file name in line: {line!r}")

    depth = _get_indent_depth(prefix)
    return name, depth


def _is_folder(name: str, has_children: bool) -> bool:
    """
    Folder detection rules:

    1. `config\\` or `config/` is always a folder.
    2. `script.py`, `README.md`, `image.png` are files.
    3. Names without an extension are folders if they have children.
       This correctly treats `Modelfile` as a file and `logs\\` as a folder.
    """
    if name.endswith("\\") or name.endswith("/"):
        return True

    if "." in PureWindowsPath(name).name or "." in PurePosixPath(name).name:
        return False

    return has_children


def parse_tree(text: str) -> list[Node]:
    """
    Converts tree text into a list of nested Node objects.
    """
    lines = [line.rstrip() for line in text.splitlines()]
    lines = [line for line in lines if line.strip()]

    if not lines:
        raise ValueError("The structure file is empty.")

    nodes: list[Node] = []
    stack: list[Node] = []

    for line in lines:
        name, depth = _extract_name(line)

        
        clean_name = name.rstrip("\\/").strip()

        if not clean_name:
            continue

        node = Node(
            name=clean_name,
            depth=depth,
        )

        
        while stack and stack[-1].depth >= depth:
            stack.pop()

        if stack:
            node.parent = stack[-1].name
            stack[-1].children.append(node)
        else:
            
            node.parent = None

        stack.append(node)
        nodes.append(node)

    for node in nodes:
        node.is_folder = _is_folder(node.name, bool(node.children))

    return nodes