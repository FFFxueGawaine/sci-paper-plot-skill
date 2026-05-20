# Sci Paper Plot Skill

Reusable Codex skill and Matplotlib templates for SCI paper figures, with an emphasis on compact mechanical dynamics and machine-learning result plots.

面向 SCI 论文图片的 Codex Skill 与 Matplotlib 模板，重点适配机械非线性动力学、系统辨识、不确定性分析和机器学习结果图。

## Overview / 简介

`sci-paper-plot-skill` helps Codex classify existing paper figures, audit exported images, trace Jupyter `savefig` sources, and create consistent publication-style Matplotlib plots.

`sci-paper-plot-skill` 可以帮助 Codex 对论文图片分类、检查已导出的图片、追踪 Jupyter Notebook 中的 `savefig` 来源，并生成风格一致的 SCI 论文图。

The default visual style is still named `MSSP Compact Dynamics`, and the Python helper module remains `scimplstyle_mssp` for compatibility.

默认视觉风格仍称为 `MSSP Compact Dynamics`，Python 辅助模块仍保留为 `scimplstyle_mssp`，方便兼容已有 demo 和代码。

## Example Figures / 示例图片

<table>
  <tr>
    <td width="50%">
      <img src="assets/examples/validation-compare.png" alt="Validation comparison">
      <br>
      <sub>Validation comparison / 验证与预测对比</sub>
    </td>
    <td width="50%">
      <img src="assets/examples/frf-compare.png" alt="FRF comparison">
      <br>
      <sub>FRF comparison / 频响函数对比</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="assets/examples/phase-poincare.png" alt="Phase portrait and Poincare section">
      <br>
      <sub>Phase and Poincare / 相图与 Poincare 截面</sub>
    </td>
    <td width="50%">
      <img src="assets/examples/time-frequency-map.png" alt="Time-frequency map">
      <br>
      <sub>Time-frequency map / 时频图</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="assets/examples/ml-confusion-matrix.png" alt="Machine learning confusion matrix">
      <br>
      <sub>Confusion matrix / 混淆矩阵</sub>
    </td>
    <td width="50%">
      <img src="assets/examples/distribution-gallery.png" alt="Distribution plots">
      <br>
      <sub>Distribution gallery / 分布类图</sub>
    </td>
  </tr>
</table>

## What It Covers / 覆盖内容

- Paper figure inventory and style audit / 论文图片清单与风格检查
- Model validation, FRF, time response, time-frequency, phase, Poincare, bifurcation, basin plots / 验证图、频响图、时域响应、时频图、相图、Poincare 图、分岔图、吸引域图
- ML result plots such as confusion matrix, ROC/PR, radar chart, feature importance, residual KDE, heatmap / 机器学习常用图，如混淆矩阵、ROC/PR、雷达图、特征重要性、残差 KDE、热力图
- Compact SCI layout rules: Times New Roman, 600 dpi PNG, careful legends, light grids, unclipped labels / 紧凑 SCI 排版：Times New Roman、600 dpi PNG、图例不遮挡数据、浅网格、坐标标签不截断

## Quick Start / 快速开始

Install dependencies:

安装依赖：

```bash
python -m pip install -r requirements.txt
```

List available demos:

查看 demo 列表：

```bash
python scripts/scimplstyle_mssp_cli.py list-demos
```

Copy demo scripts to a working folder:

复制 demo 脚本到你的工作目录：

```bash
mkdir paper-plot-workspace
python scripts/scimplstyle_mssp_cli.py copy-demos paper-plot-workspace
```

Run a copied demo:

运行复制后的 demo：

```bash
cd paper-plot-workspace
python demo_line_plot.py
```

The generated PNG files will be written to `paper-plot-workspace/output/`.

生成的 PNG 图片会写入 `paper-plot-workspace/output/`。

Audit a figure folder:

检查论文图片文件夹：

```bash
python scripts/audit_figures.py "path/to/paper/figures" --markdown
```

## Using The Style In Python / 在 Python 中使用

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, save_figure

apply_sci_style()

x = np.linspace(0.0, 10.0, 300)
y = np.sin(x) * np.exp(-0.08 * x)

fig, ax = plt.subplots(figsize=figure_size("single", 0.72), constrained_layout=True)
ax.plot(x, y, lw=1.4, label="response")
ax.set_xlabel("time (s)")
ax.set_ylabel("dis. (mm)")
panel_label(ax, "(a)")
ax.legend(frameon=True)

save_figure(fig, "example_line_plot", out_dir=Path("figures"))
```

## Recommended Working Folder / 推荐工作目录

Use the skill folder as a reusable template library. Put user-specific plotting scripts and generated figures in your own paper/project workspace, not inside the installed skill folder.

建议把 skill 文件夹当作可复用模板库。你的论文绘图脚本和生成图片应放在自己的论文/项目工作区，不要直接写入已安装的 skill 文件夹。

```text
paper-plot-workspace/
├── demo_line_plot.py
├── demo_bar_llm_performance.py
└── output/
    ├── demo_line_plot.png
    └── demo_bar_llm_performance.png
```

For Codex usage, a good prompt is:

给 Codex 使用时，可以这样说：

```text
Use $sci-paper-plot-skill. Create the plotting script and PNG output in my current project workspace, not inside the skill folder.
```

## Repository Layout / 仓库结构

```text
sci-paper-plot-skill/
├── SKILL.md
├── README.md
├── requirements.txt
├── agents/
│   └── openai.yaml
├── assets/
│   └── examples/
├── references/
└── scripts/
    ├── audit_figures.py
    ├── package_check.py
    ├── scimplstyle_mssp.py
    ├── scimplstyle_mssp_cli.py
    └── demos/
```

## Validation / 验证

Run the package check before sharing:

分享前运行包检查：

```bash
python scripts/package_check.py .
```

The package intentionally keeps only curated PNG preview images under `assets/examples/`. Demo-generated outputs should stay outside the skill folder and inside the user's working folder.

本仓库只保留 `assets/examples/` 中精选的 PNG 预览图。demo 运行后生成的图片应放在 skill 文件夹外部、用户自己的工作目录中，避免把临时输出打包进去。

## Installation As A Codex Skill / 安装为 Codex Skill

Clone this repository into your Codex skills directory:

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/FFFxueGawaine/sci-paper-plot-skill.git ~/.codex/skills/sci-paper-plot-skill
```

Then ask Codex to use:

然后可以让 Codex 使用：

```text
Use $sci-paper-plot-skill to create a compact SCI-style FRF comparison figure.
```
