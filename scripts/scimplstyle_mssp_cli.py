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


BEGINNER_GUIDE_BILINGUAL = """# sci-paper-plot-skill beginner guide / 新手向导

Use this guide when you are new to Codex plotting skills or do not know which template to choose.

如果你是小白用户，可以先不要管 Matplotlib 或 Seaborn API，直接按“我现在想做什么”选择下一步。

## 1. Pick Your Current Level / 先选当前阶段

| Level | You say | Best next step | Output |
|---|---|---|---|
| Level 1 | I have paper figures, but I do not know their types. / 我有论文图片，但不知道属于哪类图。 | Audit and classify figures first. / 先审计并分类。 | Markdown inventory and recommended categories. / 图片清单和分类建议。 |
| Level 2 | I know the target figure style, but I need a runnable example. / 我知道想画成什么样，但需要能跑的例子。 | Copy the closest demo into a project folder. / 复制最接近的 demo 到项目目录。 | A `.py` script and placeholder PNG output. / 脚本和占位数据生成图。 |
| Level 3 | I have real CSV/TXT/NPY data and want the final figure. / 我已有真实数据，想生成最终图。 | Adapt one copied demo to your real data. / 把 demo 替换成真实数据。 | Project-specific script and regenerated figure. / 项目专用脚本和最终图。 |

## 2. Commands To Start / 常用入口

```bash
python scripts/scimplstyle_mssp_cli.py audit "<paper-figure-folder>" --markdown
python scripts/scimplstyle_mssp_cli.py list-demos
python scripts/scimplstyle_mssp_cli.py copy-demos "<working-folder-outside-the-skill>"
python scripts/scimplstyle_mssp_cli.py style-guide
```

## 3. Choose A Template By Goal / 按目标选模板

| User goal | Start from | Why |
|---|---|---|
| Time response, validation curve, or method comparison / 时域响应、验证曲线、方法对比 | `demo_validation_compare.py`, `demo_line_plot.py`, `demo_hb_fig14_three_column.py` | Direct SCI-style axes, legends, and panel labels. / 直接给出论文式坐标轴、图例和子图标号。 |
| Zoomed local difference near a peak or transient / 峰值或瞬态附近局部放大 | `demo_validation_inset_zoom.py` | Keeps full trend and local detail in one figure. / 同时保留整体趋势和局部细节。 |
| Error distribution or uncertainty / 误差分布、不确定性、后验密度 | `demo_error_boxplot.py`, `demo_kde_uncertainty.py`, `demo_matplotlib_distribution_gallery.py` | Good for repeated trials, posterior density, and uncertainty checks. / 适合重复试验、后验密度和不确定性检查。 |
| Frequency response or time-frequency result / 频响或时频图 | `demo_frf_compare.py`, `demo_time_frequency_map.py` | Uses engineering labels, colorbars, and compact layout. / 已带工程标签、色条和紧凑排版。 |
| Common Matplotlib plot types / 常见 Matplotlib 图 | `demo_matplotlib_relation_gallery.py`, `demo_matplotlib_categorical_gallery.py`, `demo_matplotlib_field_gallery.py`, `demo_matplotlib_3d_surface.py` | Best when final manuscript layout needs precise Matplotlib control. / 适合最终论文图，需要精确控制布局。 |
| Common Seaborn/DataFrame plots / 常见 Seaborn 表格数据图 | `demo_seaborn_common_gallery.py` | Best when data is already a tidy table with group columns. / 适合已有分组列的表格数据。 |
| Machine-learning result figure / 机器学习结果图 | `demo_ml_classification_curves.py`, `demo_ml_confusion_matrix.py`, `demo_ml_feature_importance.py`, `demo_ml_hyperparameter_heatmap.py` | Covers common ML evaluation plots without starting from scratch. / 覆盖常用模型评价图。 |
| Hierarchical Bayesian clearance-system paper templates / 层级贝叶斯间隙非线性论文模板 | `demo_hb_clearance_templates.py`, `demo_hb_fig14_three_column.py` | Paper-specific Fig. 1-Fig. 18 style mapping. / 对应该论文 Fig. 1-Fig. 18 的模板映射。 |

## 4. Ask Codex Like This / 可以这样问 Codex

```text
Use $sci-paper-plot-skill. I am a beginner. Please audit my figure folder and tell me which demo is closest.
```

```text
Use $sci-paper-plot-skill. I do not know which plot type to choose. Please recommend one template based on my goal before writing code.
```

```text
Use $sci-paper-plot-skill. Please copy the closest demo to my current project folder and run it with placeholder data first.
```

## 5. Safe Defaults / 安全默认规则

- Do not edit original paper images during the first pass.
- Do not write generated figures into the installed skill folder.
- Start with one figure type before converting a whole paper.
- Use Matplotlib for final journal layout; use Seaborn for grouped table data and quick faceting.
"""


BEGINNER_GUIDE_ZH = """# sci-paper-plot-skill 新手向导

如果你是小白用户，可以先不要管 Matplotlib 或 Seaborn API，直接按“我现在想做什么”选择下一步。

## 1. 先选当前阶段

| 阶段 | 你的情况 | 下一步 | 输出 |
|---|---|---|---|
| Level 1 | 我有论文图片，但不知道属于哪类图。 | 先审计并分类。 | 图片清单和分类建议。 |
| Level 2 | 我知道想画成什么样，但需要能跑的例子。 | 复制最接近的 demo 到项目目录。 | 脚本和占位数据生成图。 |
| Level 3 | 我已有真实 CSV/TXT/NPY 数据，想生成最终图。 | 把 demo 替换成真实数据。 | 项目专用脚本和最终图。 |

## 2. 常用入口

```bash
python scripts/scimplstyle_mssp_cli.py audit "<论文图片文件夹>" --markdown
python scripts/scimplstyle_mssp_cli.py list-demos
python scripts/scimplstyle_mssp_cli.py beginner-guide --lang zh
python scripts/scimplstyle_mssp_cli.py recommend "误差分布" --lang zh
python scripts/scimplstyle_mssp_cli.py copy-demos "<skill 外部的工作文件夹>"
```

## 3. 按目标选模板

| 目标 | 推荐起点 | 适用原因 |
|---|---|---|
| 时域响应、验证曲线、方法对比 | `demo_validation_compare.py`, `demo_line_plot.py`, `demo_hb_fig14_three_column.py` | 直接给出论文式坐标轴、图例和子图标号。 |
| 峰值或瞬态附近局部放大 | `demo_validation_inset_zoom.py` | 同时保留整体趋势和局部细节。 |
| 误差分布、不确定性、后验密度 | `demo_error_boxplot.py`, `demo_kde_uncertainty.py`, `demo_matplotlib_distribution_gallery.py` | 适合重复试验、后验密度和不确定性检查。 |
| 频响或时频图 | `demo_frf_compare.py`, `demo_time_frequency_map.py` | 已带工程标签、色条和紧凑排版。 |
| 常见 Matplotlib 论文图 | `demo_matplotlib_relation_gallery.py`, `demo_matplotlib_categorical_gallery.py`, `demo_matplotlib_field_gallery.py` | 适合最终论文图，需要精确控制布局。 |
| 常见 Seaborn 表格数据图 | `demo_seaborn_common_gallery.py` | 适合已有分组列的表格数据。 |
| 机器学习结果图 | `demo_ml_classification_curves.py`, `demo_ml_confusion_matrix.py`, `demo_ml_feature_importance.py` | 覆盖常见模型对比和评价图。 |

## 4. 可以这样问 Codex

```text
Use $sci-paper-plot-skill. 我是新手，请先审计我的图片文件夹，并告诉我最接近哪个 demo。
```

```text
Use $sci-paper-plot-skill. 我不知道该选哪个图，请先根据我的目标推荐模板，不要直接写代码。
```

## 5. 安全默认规则

- 第一轮不改原始论文图片。
- 不把生成图写进已安装的 skill 文件夹。
- 先完成一类图，再扩展到整篇论文。
- 最终论文排版优先 Matplotlib；已有分组表格数据优先 Seaborn。
"""


BEGINNER_GUIDE_EN = """# sci-paper-plot-skill beginner guide

Use this guide when you are new to Codex plotting skills or do not know which template to choose.

## 1. Pick Your Current Level

| Level | You say | Best next step | Output |
|---|---|---|---|
| Level 1 | I have paper figures, but I do not know their types. | Audit and classify figures first. | Markdown inventory and recommended categories. |
| Level 2 | I know the target figure style, but I need a runnable example. | Copy the closest demo into a project folder. | A `.py` script and placeholder PNG output. |
| Level 3 | I have real CSV/TXT/NPY data and want the final figure. | Adapt one copied demo to your real data. | Project-specific script and regenerated figure. |

## 2. Commands To Start

```bash
python scripts/scimplstyle_mssp_cli.py audit "<paper-figure-folder>" --markdown
python scripts/scimplstyle_mssp_cli.py list-demos
python scripts/scimplstyle_mssp_cli.py beginner-guide --lang en
python scripts/scimplstyle_mssp_cli.py recommend "time response" --lang en
python scripts/scimplstyle_mssp_cli.py copy-demos "<working-folder-outside-the-skill>"
```

## 3. Choose A Template By Goal

| User goal | Start from | Why |
|---|---|---|
| Time response, validation curve, or method comparison | `demo_validation_compare.py`, `demo_line_plot.py`, `demo_hb_fig14_three_column.py` | Direct SCI-style axes, legends, and panel labels. |
| Zoomed local difference near a peak or transient | `demo_validation_inset_zoom.py` | Keeps full trend and local detail in one figure. |
| Error distribution or uncertainty | `demo_error_boxplot.py`, `demo_kde_uncertainty.py`, `demo_matplotlib_distribution_gallery.py` | Good for repeated trials, posterior density, and uncertainty checks. |
| Frequency response or time-frequency result | `demo_frf_compare.py`, `demo_time_frequency_map.py` | Uses engineering labels, colorbars, and compact layout. |
| Common Matplotlib plot types | `demo_matplotlib_relation_gallery.py`, `demo_matplotlib_categorical_gallery.py`, `demo_matplotlib_field_gallery.py` | Best when final manuscript layout needs precise Matplotlib control. |
| Common Seaborn/DataFrame plots | `demo_seaborn_common_gallery.py` | Best when data is already a tidy table with group columns. |
| Machine-learning result figure | `demo_ml_classification_curves.py`, `demo_ml_confusion_matrix.py`, `demo_ml_feature_importance.py` | Covers common model-comparison and evaluation figures. |
"""


BEGINNER_GUIDES = {
    "zh": BEGINNER_GUIDE_ZH,
    "en": BEGINNER_GUIDE_EN,
    "bilingual": BEGINNER_GUIDE_BILINGUAL,
}


CURATED_SET_NAME = "curated"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


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
    write_or_print(BEGINNER_GUIDES[args.lang], args.output)


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
    beginner_guide.add_argument("--lang", choices=sorted(BEGINNER_GUIDES), default="zh", help="Guide language")
    beginner_guide.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    beginner_guide.set_defaults(func=command_beginner_guide)

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
