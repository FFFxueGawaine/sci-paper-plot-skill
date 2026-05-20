# -*- coding: utf-8 -*-
"""Command entry point for the scimplstyle_mssp skill."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from audit_figures import build_inventory, markdown_table


STYLE_GUIDE = """# scimplstyle_mssp quick style guide

Style name: MSSP Compact Dynamics.

- Font: Times New Roman, mathtext STIX.
- Export: PNG bitmap at 600 dpi by default; generate PDF/SVG only when explicitly requested.
- Width: single column 85 mm; double column 178 mm.
- Units: write `time (s)`, `fre. (Hz)`, `dis. (mm)`, `mag. (dB)`.
- Labels: prefer lowercase compact quantities such as `vel.`, `acc.`, `amp.`, `err.`, `rmse`; keep official unit capitalization such as `Hz`, `N`, `MPa`, `dB`.
- Panel labels: bold `(a)`, `(b)`, `(c)` above each axes.
- Legends: prefer `safe_legend()`; place dense legends outside the axes or in a genuinely empty corner.
- Grid: keep it light, behind data, and disable the axis direction that does not help reading.
- Validation plots: experiment in black or blue; identified/proposed in red dashed.
- KDE plots: use density colorbar, true/estimated markers, compact RE annotations.
- FRF plots: use blue/black/red line hierarchy and dB magnitude.
- Nonlinear dynamics demos: use Duffing, Van der Pol, pendulum, Bouc-Wen, restoring-force, and sparse-library plots as template anchors.
- ML plots: prefer bar/box/heatmap for precise comparison; use radar charts only as compact summary views.
- Confusion matrices and heatmaps: annotate compactly and keep colorbars with explicit units.
- Gallery figures: choose the plot family by manuscript purpose; avoid decorative chart types when a line, bar, or boxplot is clearer.
"""


def command_audit(args: argparse.Namespace) -> None:
    inventory = build_inventory(args.root)
    text = markdown_table(inventory) if args.markdown else inventory
    if args.markdown:
        write_or_print(text, args.output)
    else:
        import json

        write_or_print(json.dumps(text, ensure_ascii=False, indent=2), args.output)


def command_style_guide(args: argparse.Namespace) -> None:
    write_or_print(STYLE_GUIDE, args.output)


def command_list_demos(_: argparse.Namespace) -> None:
    demo_dir = Path(__file__).resolve().parent / "demos"
    for path in sorted(demo_dir.glob("demo_*.py")):
        print(path.name)


def command_copy_demos(args: argparse.Namespace) -> None:
    demo_dir = Path(__file__).resolve().parent / "demos"
    args.output.mkdir(parents=True, exist_ok=True)
    for path in sorted(demo_dir.glob("demo_*.py")):
        shutil.copy2(path, args.output / path.name)
    print(args.output)


def write_or_print(text: str, output: Path | None) -> None:
    if output:
        output.write_text(text.rstrip() + "\n", encoding="utf-8")
    else:
        print(text.rstrip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Inspect exported figures and notebook savefig calls")
    audit.add_argument("root", type=Path, help="Paper directory to inspect")
    audit.add_argument("--markdown", action="store_true", help="Print Markdown table")
    audit.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    audit.set_defaults(func=command_audit)

    style_guide = subparsers.add_parser("style-guide", help="Print the compact SCI style guide")
    style_guide.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    style_guide.set_defaults(func=command_style_guide)

    list_demos = subparsers.add_parser("list-demos", help="List available demo scripts")
    list_demos.set_defaults(func=command_list_demos)

    copy_demos = subparsers.add_parser("copy-demos", help="Copy demo scripts to a user working folder")
    copy_demos.add_argument("output", type=Path, help="Destination folder outside the skill package")
    copy_demos.set_defaults(func=command_copy_demos)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
