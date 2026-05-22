# -*- coding: utf-8 -*-
"""Command entry point for the scimplstyle_mssp skill."""

from __future__ import annotations

import argparse
import json
import subprocess
import shutil
import sys
from pathlib import Path

from audit_figures import build_inventory, markdown_table


STYLE_GUIDE = """# scimplstyle_mssp quick style guide

Style name: MSSP Compact Dynamics.

- Font: Times New Roman, mathtext STIX.
- Export: PNG bitmap at 600 dpi by default; generate PDF/SVG only when explicitly requested.
- Width: single column 85 mm; double column 178 mm.
- Units: write `time (s)`, `fre. (Hz)`, `dis. (mm)`, `mag. (dB)`.
- Unknown units: omit the unit; do not use `(-)` as a placeholder. Use `format_axis_label(label, unit)` for this rule.
- Labels: prefer lowercase compact quantities such as `vel.`, `acc.`, `amp.`, `err.`, `rmse`; keep official unit capitalization such as `Hz`, `N`, `MPa`, `dB`.
- Panel labels: bold `(a)`, `(b)`, `(c)` above each axes.
- Legends: prefer `safe_legend()`; place dense legends outside the axes or in a genuinely empty corner.
- Grid: keep it light, behind data, and disable the axis direction that does not help reading.
- Validation plots: experiment in black or blue; identified/proposed in red dashed.
- Local zoom plots: use `add_zoom_inset()` for small peak, transient, or resonance differences; keep inset ticks compact/inward, reserve blank parent-axes space, and omit duplicate inset legends.
- KDE plots: use density colorbar, true/estimated markers, compact RE annotations.
- FRF plots: use blue/black/red line hierarchy and dB magnitude.
- Nonlinear dynamics demos: use Duffing, Van der Pol, pendulum, Bouc-Wen, restoring-force, and sparse-library plots as template anchors.
- ML plots: prefer bar/box/heatmap for precise comparison; use radar charts only as compact summary views.
- Confusion matrices and heatmaps: annotate compactly and keep colorbars with explicit units.
- Gallery figures: choose the plot family by manuscript purpose; avoid decorative chart types when a line, bar, or boxplot is clearer.
- Hierarchical Bayesian clearance paper: use `references/hb-clearance-paper-figure-templates.md` and `demo_hb_clearance_templates.py` for Fig. 1-Fig. 18 template coverage.
"""


BEGINNER_GUIDE_FILES = {
    "zh": ["references/codex-beginner-guide.zh-CN.md"],
    "en": ["references/codex-beginner-guide.en.md"],
    "bilingual": [
        "references/codex-beginner-guide.zh-CN.md",
        "references/codex-beginner-guide.en.md",
    ],
}


PRE_RUN_BRIEF_FILES = {
    "zh": ["references/pre-run-brief.zh-CN.md"],
    "en": ["references/pre-run-brief.en.md"],
    "bilingual": [
        "references/pre-run-brief.zh-CN.md",
        "references/pre-run-brief.en.md",
    ],
}


CURATED_SET_NAME = "curated"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_reference_text(rel_path: str) -> str:
    path = skill_root() / rel_path
    return path.read_text(encoding="utf-8").rstrip()


def read_reference_group(rel_paths: list[str]) -> str:
    return "\n\n---\n\n".join(read_reference_text(rel_path) for rel_path in rel_paths)


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


def command_beginner_guide(args: argparse.Namespace) -> None:
    write_or_print(read_reference_group(BEGINNER_GUIDE_FILES[args.lang]), args.output)


def command_run_brief(args: argparse.Namespace) -> None:
    write_or_print(read_reference_group(PRE_RUN_BRIEF_FILES[args.lang]), args.output)


def load_demo_index(root: Path | None = None) -> list[dict[str, object]]:
    root = root or skill_root()
    path = root / "references" / "demo-index.json"
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return list(payload["demos"])


def demo_priority(entry: dict[str, object]) -> int:
    value = entry.get("priority", 0)
    return int(value) if isinstance(value, int) else 0


def select_demo_entries(demo_set: str) -> list[dict[str, object]]:
    demos = load_demo_index()
    if demo_set == "all":
        return demos
    return [demo for demo in demos if bool(demo.get("curated"))]


def score_demo(query: str, entry: dict[str, object]) -> tuple[int, list[str]]:
    query_norm = query.casefold().strip()
    if not query_norm:
        return 0, []
    terms: list[str] = []
    for field in ["keywords_zh", "keywords_en", "plot_types", "goals_zh", "goals_en"]:
        value = entry.get(field, [])
        if isinstance(value, list):
            terms.extend(str(item) for item in value)
        elif isinstance(value, str):
            terms.append(value)
    matches: list[str] = []
    score = 0
    for term in terms:
        term_norm = term.casefold().strip()
        if not term_norm:
            continue
        if term_norm in query_norm or query_norm in term_norm:
            score += 5 if any("\u4e00" <= char <= "\u9fff" for char in term_norm) else 4
            matches.append(term)
    for token in query_norm.replace("_", " ").replace("-", " ").split():
        if len(token) < 3:
            continue
        haystack = " ".join(terms).casefold()
        if token in haystack and token not in [m.casefold() for m in matches]:
            score += 2
            matches.append(token)
    if bool(entry.get("curated")) and score > 0:
        score += 1
    score += min(demo_priority(entry), 3)
    return score, matches[:5]


def format_recommendations(query: str, ranked: list[tuple[int, list[str], dict[str, object]]], lang: str, top: int) -> str:
    visible = ranked[:top]
    if lang == "en":
        lines = [f"# Recommended demos for `{query}`", ""]
        if not visible or visible[0][0] <= 0:
            lines.append("No strong keyword match was found. Showing curated starter demos.")
            lines.append("")
        lines.append("| Rank | Demo | Why | Next command |")
        lines.append("|---|---|---|---|")
        for index, (score, matches, demo) in enumerate(visible, start=1):
            why = str(demo.get("goals_en", ["General SCI-style figure"])[0])
            if matches:
                why += f"; matched: {', '.join(matches)}"
            command = f"python scripts/scimplstyle_mssp_cli.py copy-demos <working-folder>"
            lines.append(f"| {index} | `{demo['file']}` | {why} | `{command}` |")
        return "\n".join(lines)

    lines = [f"# `{query}` 的推荐模板", ""]
    if not visible or visible[0][0] <= 0:
        lines.append("没有找到强关键词匹配，下面先给出适合小白起步的精选模板。")
        lines.append("")
    lines.append("| 排名 | 推荐 demo | 推荐理由 | 下一步命令 |")
    lines.append("|---|---|---|---|")
    for index, (score, matches, demo) in enumerate(visible, start=1):
        goals = demo.get("goals_zh", ["通用 SCI 论文图"])
        why = str(goals[0] if isinstance(goals, list) and goals else goals)
        if matches:
            why += f"；匹配词：{', '.join(matches)}"
        command = "python scripts/scimplstyle_mssp_cli.py copy-demos <工作文件夹>"
        lines.append(f"| {index} | `{demo['file']}` | {why} | `{command}` |")
    lines.extend(
        [
            "",
            "建议：先复制 demo 到 skill 外部的项目目录，跑通占位数据，再替换成真实数据。",
        ]
    )
    return "\n".join(lines)


def command_recommend(args: argparse.Namespace) -> None:
    demos = load_demo_index()
    ranked = []
    for demo in demos:
        score, matches = score_demo(args.query, demo)
        ranked.append((score, matches, demo))
    ranked.sort(key=lambda item: (item[0], demo_priority(item[2]), bool(item[2].get("curated"))), reverse=True)
    text = format_recommendations(args.query, ranked, args.lang, args.top)
    write_or_print(text, args.output)


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


def run_preview_gallery(output: Path, demo_set: str, timeout: int) -> dict[str, object]:
    root = skill_root()
    entries = select_demo_entries(demo_set)
    output = output.resolve()
    run_root = output / "_preview_run"
    run_scripts = run_root / "scripts"
    run_demos = run_scripts / "demos"
    run_output = run_demos / "output"
    figures = output / "figures"
    for directory in [run_demos, figures]:
        directory.mkdir(parents=True, exist_ok=True)
    if run_output.exists():
        shutil.rmtree(run_output)
    run_output.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "scripts" / "scimplstyle_mssp.py", run_scripts / "scimplstyle_mssp.py")

    logs: list[str] = []
    failures: list[str] = []
    for entry in entries:
        demo_file = str(entry["file"])
        src = root / "scripts" / "demos" / demo_file
        dst = run_demos / demo_file
        shutil.copy2(src, dst)
        completed = subprocess.run(
            [sys.executable, str(dst)],
            cwd=str(run_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        logs.append(f"## {demo_file}\n\nreturncode: {completed.returncode}\n\nstdout:\n{completed.stdout}\n\nstderr:\n{completed.stderr}\n")
        if completed.returncode != 0:
            failures.append(demo_file)

    copied: list[str] = []
    for png in sorted(run_output.glob("*.png")):
        target = figures / png.name
        shutil.copy2(png, target)
        copied.append(target.name)

    index_lines = [
        "# Demo Preview Gallery",
        "",
        f"- Demo set: `{demo_set}`",
        f"- Demos run: {len(entries)}",
        f"- PNG files: {len(copied)}",
        "",
    ]
    for name in copied:
        index_lines.append(f"## {name}")
        index_lines.append("")
        index_lines.append(f"![{name}](figures/{name})")
        index_lines.append("")
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    (output / "execution-log.md").write_text("\n\n".join(logs).rstrip() + "\n", encoding="utf-8")
    return {
        "output": str(output),
        "index": str(output / "index.md"),
        "figures": copied,
        "failures": failures,
        "demo_count": len(entries),
    }


def command_preview_gallery(args: argparse.Namespace) -> None:
    result = run_preview_gallery(args.output, args.demo_set, args.timeout)
    if result["failures"]:
        write_or_print(json.dumps(result, ensure_ascii=False, indent=2), None)
        raise SystemExit(1)
    if args.lang == "en":
        text = f"Preview gallery generated: {result['index']}\nPNG files: {len(result['figures'])}"
    else:
        text = f"预览图册已生成：{result['index']}\nPNG 数量：{len(result['figures'])}"
    write_or_print(text, None)


def inspect_png(path: Path) -> dict[str, object]:
    from PIL import Image

    size_bytes = path.stat().st_size
    with Image.open(path) as img:
        width, height = img.size
        extrema = img.convert("RGB").getextrema()
    channel_ranges = [max_value - min_value for min_value, max_value in extrema]
    nonblank = max(channel_ranges) > 2
    ok = size_bytes > 1024 and width >= 100 and height >= 100 and nonblank
    return {
        "file": path.name,
        "width": width,
        "height": height,
        "bytes": size_bytes,
        "nonblank": nonblank,
        "ok": ok,
    }


def format_check_report(records: list[dict[str, object]], result: dict[str, object], output_format: str) -> str:
    if output_format == "json":
        return json.dumps({"gallery": result, "checks": records}, ensure_ascii=False, indent=2)
    lines = [
        "# Demo Visual Check",
        "",
        f"- Gallery: `{result['index']}`",
        f"- PNG files: {len(records)}",
        f"- Passed: {sum(1 for item in records if item['ok'])}",
        "",
        "| File | Size | Bytes | Nonblank | Status |",
        "|---|---:|---:|---|---|",
    ]
    for item in records:
        status = "OK" if item["ok"] else "FAIL"
        lines.append(f"| `{item['file']}` | {item['width']} x {item['height']} | {item['bytes']} | {item['nonblank']} | {status} |")
    return "\n".join(lines)


def command_check_demos(args: argparse.Namespace) -> None:
    result = run_preview_gallery(args.output, args.demo_set, args.timeout)
    figures = args.output.resolve() / "figures"
    records = [inspect_png(path) for path in sorted(figures.glob("*.png"))]
    text = format_check_report(records, result, args.format)
    if args.output_report:
        args.output_report.write_text(text.rstrip() + "\n", encoding="utf-8")
    write_or_print(text, None)
    if result["failures"] or not records or any(not item["ok"] for item in records):
        raise SystemExit(1)


def write_or_print(text: str, output: Path | None) -> None:
    if output:
        output.write_text(text.rstrip() + "\n", encoding="utf-8")
    else:
        if hasattr(sys.stdout, "buffer"):
            sys.stdout.buffer.write((text.rstrip() + "\n").encode("utf-8"))
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

    beginner_guide = subparsers.add_parser("beginner-guide", help="Print the beginner template-selection guide")
    beginner_guide.add_argument("--lang", choices=sorted(BEGINNER_GUIDE_FILES), default="zh", help="Guide language")
    beginner_guide.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    beginner_guide.set_defaults(func=command_beginner_guide)

    run_brief = subparsers.add_parser("run-brief", help="Print the pre-run user prompt checklist")
    run_brief.add_argument("--lang", choices=sorted(PRE_RUN_BRIEF_FILES), default="zh", help="Brief language")
    run_brief.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    run_brief.set_defaults(func=command_run_brief)

    recommend = subparsers.add_parser("recommend", help="Recommend demo templates by a natural-language goal")
    recommend.add_argument("query", help="Plot goal, e.g. 误差分布 or time response")
    recommend.add_argument("--lang", choices=["zh", "en"], default="zh", help="Output language")
    recommend.add_argument("--top", type=int, default=5, help="Number of recommendations")
    recommend.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    recommend.set_defaults(func=command_recommend)

    preview = subparsers.add_parser("preview-gallery", help="Generate a demo preview gallery outside the skill package")
    preview.add_argument("output", type=Path, help="Output folder outside the skill package")
    preview.add_argument("--set", dest="demo_set", choices=[CURATED_SET_NAME, "all"], default=CURATED_SET_NAME, help="Demo set to run")
    preview.add_argument("--lang", choices=["zh", "en"], default="zh", help="Output language")
    preview.add_argument("--timeout", type=int, default=180, help="Timeout per demo in seconds")
    preview.set_defaults(func=command_preview_gallery)

    check = subparsers.add_parser("check-demos", help="Generate and visually check demo PNG outputs")
    check.add_argument("output", type=Path, help="Output folder outside the skill package")
    check.add_argument("--set", dest="demo_set", choices=[CURATED_SET_NAME, "all"], default=CURATED_SET_NAME, help="Demo set to run")
    check.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Report format")
    check.add_argument("--output-report", type=Path, help="Optional UTF-8 report path")
    check.add_argument("--timeout", type=int, default=180, help="Timeout per demo in seconds")
    check.set_defaults(func=command_check_demos)

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
