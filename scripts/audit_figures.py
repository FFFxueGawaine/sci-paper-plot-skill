# -*- coding: utf-8 -*-
"""Read-only inventory of exported paper figures and notebook savefig calls."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from PIL import Image


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
SAVEFIG_RE = re.compile(r"(?:plt\.)?savefig\((?P<args>[^)]*)\)")
QUOTED_PATH_RE = re.compile(r"['\"]([^'\"]+)['\"]")


def image_info(path: Path, root: Path) -> dict[str, Any]:
    with Image.open(path) as img:
        dpi = img.info.get("dpi") or (None, None)
        dpi_x, dpi_y = dpi if isinstance(dpi, tuple) and len(dpi) >= 2 else (None, None)
        return {
            "path": str(path),
            "case": relative_case(path, root),
            "extension": path.suffix.lower(),
            "width": img.width,
            "height": img.height,
            "dpi_x": round(float(dpi_x), 1) if dpi_x else None,
            "dpi_y": round(float(dpi_y), 1) if dpi_y else None,
            "bytes": path.stat().st_size,
        }


def relative_case(path: Path, root: Path) -> str:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return ""
    return rel.parts[0] if len(rel.parts) > 1 else ""


def notebook_savefigs(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    found: list[dict[str, Any]] = []
    for cell_index, cell in enumerate(nb.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        for line_index, line in enumerate(source.splitlines(), start=1):
            if "savefig" not in line or line.lstrip().startswith("#"):
                continue
            match = SAVEFIG_RE.search(line)
            if not match:
                continue
            quoted = QUOTED_PATH_RE.search(match.group("args"))
            target = quoted.group(1) if quoted else ""
            found.append(
                {
                    "notebook": str(path),
                    "cell": cell_index,
                    "line": line_index,
                    "target": target,
                    "code": line.strip(),
                }
            )
    return found


def build_inventory(root: Path) -> dict[str, Any]:
    images = [
        image_info(path, root)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS
    ]
    savefigs: list[dict[str, Any]] = []
    for notebook in sorted(root.rglob("*.ipynb")):
        savefigs.extend(notebook_savefigs(notebook))
    return {"root": str(root), "images": images, "savefigs": savefigs}


def markdown_table(inventory: dict[str, Any]) -> str:
    savefig_by_name: dict[str, list[str]] = {}
    for item in inventory["savefigs"]:
        target = Path(item["target"]).name
        if not target:
            continue
        savefig_by_name.setdefault(target.lower(), []).append(
            f"{item['notebook']} cell {item['cell']} line {item['line']}"
        )

    lines = [
        "| Figure | Case | Format | Pixels | DPI | Source savefig |",
        "|---|---|---|---|---|---|",
    ]
    for image in inventory["images"]:
        name = Path(image["path"]).name
        dpi = (
            f"{image['dpi_x']}x{image['dpi_y']}"
            if image["dpi_x"] and image["dpi_y"]
            else "unknown"
        )
        sources = "<br>".join(savefig_by_name.get(name.lower(), [])) or "not found"
        lines.append(
            "| {path} | {case} | {ext} | {width}x{height} | {dpi} | {sources} |".format(
                path=image["path"],
                case=image["case"],
                ext=image["extension"],
                width=image["width"],
                height=image["height"],
                dpi=dpi,
                sources=sources,
            )
        )
    return "\n".join(lines)


def write_stdout(text: str) -> None:
    """Write UTF-8 text even when the Windows console defaults to GBK."""
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Paper directory to inspect")
    parser.add_argument("--markdown", action="store_true", help="Print Markdown table")
    parser.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    args = parser.parse_args()

    inventory = build_inventory(args.root)
    text = markdown_table(inventory) if args.markdown else json.dumps(inventory, ensure_ascii=False, indent=2)

    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        write_stdout(text)


if __name__ == "__main__":
    main()
