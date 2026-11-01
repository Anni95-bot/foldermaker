from pathlib import Path

from .parser import parse_tree


def build_from_text(
    tree_text: str,
    output_dir: str | Path = ".",
    dry_run: bool = False,
) -> list[str]:
    output_path = Path(output_dir).expanduser().resolve()
    nodes = parse_tree(tree_text)

    created: list[str] = []
    node_map = {node.name: node for node in nodes}

    for node in nodes:
        relative_path = _get_relative_path(node, node_map)
        target = output_path / relative_path

        if node.is_folder:
            _create_folder(target, dry_run, created)
        else:
            _create_file(target, dry_run, created)

    return created


def build(
    structure_file: str | Path,
    output_dir: str | Path = ".",
    dry_run: bool = False,
) -> list[str]:
    """
    Reads a .txt file containing a folder tree and creates it.

    Example:
        import folderforge
        folderforge.build("structure.txt", output_dir="D:/MY_AGENT")
    """
    structure_path = Path(structure_file).expanduser().resolve()

    if not structure_path.exists():
        raise FileNotFoundError(f"Structure file not found: {structure_path}")

    tree_text = structure_path.read_text(encoding="utf-8")
    return build_from_text(tree_text, output_dir=output_dir, dry_run=dry_run)


def _get_relative_path(node, node_map) -> Path:
    """
    Builds the full relative path, such as:
    core/ollama_client.py
    """
    parts = [node.name]
    current = node

    while current.parent:
        parent = node_map.get(current.parent)

        if parent is None:
            break

        parts.append(parent.name)
        current = parent

    return Path(*reversed(parts))


def _create_folder(path: Path, dry_run: bool, created: list[str]) -> None:
    if dry_run:
        print(f"[DRY RUN] Would create folder: {path}")
        created.append(str(path))
        return

    path.mkdir(parents=True, exist_ok=True)
    print(f"Created folder: {path}")
    created.append(str(path))


def _create_file(path: Path, dry_run: bool, created: list[str]) -> None:
    if dry_run:
        print(f"[DRY RUN] Would create file: {path}")
        created.append(str(path))
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.touch()
        print(f"Created file: {path}")
    else:
        print(f"File already exists: {path}")

    created.append(str(path))


def cli():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create folders and files from a text folder-tree structure."
    )
    parser.add_argument("structure_file", help="Path to the .txt tree file")
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory where the structure will be created"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating anything"
    )

    args = parser.parse_args()

    build(
        structure_file=args.structure_file,
        output_dir=args.output,
        dry_run=args.dry_run,
    )