# -*- coding: utf-8 -*-
"""Command entry point for the scimplstyle_mssp skill."""

from __future__ import annotations

import argparse
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


BEGINNER_GUIDE = """# sci-paper-plot-skill beginner guide / 新手向导

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
    write_or_print(BEGINNER_GUIDE, args.output)


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
    beginner_guide.add_argument("--output", type=Path, help="Optional UTF-8 output path")
    beginner_guide.set_defaults(func=command_beginner_guide)

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
