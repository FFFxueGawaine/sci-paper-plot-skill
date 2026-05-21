# Sci Paper Plot Skill

Reusable Codex skill for turning SCI paper figures into classified, reusable Matplotlib templates.

面向 SCI 论文绘图的 Codex Skill：把论文图片按“论文功能”分类，再沉淀为可复用的 Matplotlib 模板。

## What Problem It Solves / 解决什么问题

科研绘图常见的问题不是“不会画一张图”，而是：

- 同一篇论文里图片风格不统一；
- 旧 Notebook 里 `savefig` 分散，难以复现；
- 看到一篇好论文的图，只能临摹，不能沉淀成模板；
- 论文图类型很多，缺少“图的功能分类”和对应模板。

This skill solves that by combining figure audit, role-based classification, and reusable plotting demos.

本 skill 的做法是：先审计图片，再按论文功能分类，最后把每类图沉淀成可运行 demo。

## Core Innovation / 方式与创新点

1. **Classify by manuscript role, not file type.**  
   A figure is treated as validation, posterior density, candidate-library selection, FRF, time-frequency map, schematic, and so on. This makes template reuse more reliable than simply matching `.jpg` or `.png`.

2. **Turn paper figures into template functions.**  
   The skill does not store a paper's original figures as the main asset. It creates reusable Matplotlib functions with synthetic placeholder data, then users replace the arrays with real data.

3. **Keep style and scientific meaning together.**  
   Templates preserve axis semantics, units, panel labels, density meaning, uncertainty meaning, and validation hierarchy instead of only copying colors and fonts.

4. **Use a self-learning loop.**  
   For a new paper, Codex can audit figures, classify them, create a figure-template map, add demos, and validate the package. The skill becomes better after each curated paper.

## Built-In Example / 内置论文示例

The current paper-specific example is:

- Yusheng Wang, Hui Qian, Qinghua Liu, Yinhang Ma, Dong Jiang. **Hierarchical Bayesian model for identifying clearance-type nonlinear system**. *Mechanical Systems and Signal Processing*, 235, 112891, 2025.
- DOI: [10.1016/j.ymssp.2025.112891](https://doi.org/10.1016/j.ymssp.2025.112891)
- ScienceDirect: [article page](https://www.sciencedirect.com/science/article/abs/pii/S0888327025005928)

Resources:

- `references/hb-clearance-paper-figure-templates.md` - Fig. 1-Fig. 18 classification and template map.
- `scripts/demos/demo_hb_clearance_templates.py` - one runnable template function set for Fig. 1-Fig. 18.
- `scripts/demos/demo_hb_fig14_three_column.py` - Fig. 14-style one-row three-column response demo.

## Recommended Installation / 建议安装方式

Install as a Codex skill by cloning the repository into the Codex skills folder:

```bash
git clone https://github.com/FFFxueGawaine/sci-paper-plot-skill.git ~/.codex/skills/sci-paper-plot-skill
```

Then install runtime dependencies:

```bash
cd ~/.codex/skills/sci-paper-plot-skill
python -m pip install -r requirements.txt
```

After installation, ask Codex:

```text
Use $sci-paper-plot-skill to classify my paper figures and create reusable Matplotlib templates.
```

For updates:

```bash
cd ~/.codex/skills/sci-paper-plot-skill
git pull
```

## Quick Use / 快速使用

Audit exported paper figures and Notebook `savefig` calls:

```bash
python scripts/audit_figures.py "path/to/paper/figures" --markdown
```

List available demos:

```bash
python scripts/scimplstyle_mssp_cli.py list-demos
```

Copy demos to a working folder:

```bash
python scripts/scimplstyle_mssp_cli.py copy-demos paper-plot-workspace
```

Run the clearance-paper full template set:

```bash
python scripts/demos/demo_hb_clearance_templates.py
```

Run the Fig. 14 one-row three-column demo:

```bash
python scripts/demos/demo_hb_fig14_three_column.py
```

## Self-Learning Method / Skill 自学习方法

When adding a new reference paper, use this workflow:

1. **Audit / 审计**  
   Run `scripts/audit_figures.py` on the paper folder. Collect figure names, image sizes, DPI, and Notebook `savefig` sources.

2. **Classify / 分类**  
   Map each figure to the taxonomy in `SKILL.md`, such as validation, posterior density, candidate-library selection, time-frequency map, schematic, or uncertainty plot.

3. **Create a paper map / 建立逐图映射**  
   Add a reference file under `references/`, for example `references/<paper-name>-figure-templates.md`. Record figure number, category, manuscript role, source family, template function, and style notes.

4. **Add runnable demos / 添加可运行模板**  
   Add one or more scripts under `scripts/demos/`. Use synthetic placeholder data. Do not copy private project data into the skill package.

5. **Register / 注册入口**  
   Add the new paper and demo names to this README and, if needed, add new taxonomy terms to `SKILL.md`.

6. **Validate / 验证**  
   Run:

   ```bash
   python scripts/package_check.py .
   ```

7. **Use outside the skill folder / 在项目目录使用**  
   Treat the skill as a template library. Put real paper plotting scripts and generated figures in the user's project folder, not inside the installed skill package.

## Repository Layout / 仓库结构

```text
sci-paper-plot-skill/
├── SKILL.md
├── README.md
├── requirements.txt
├── assets/examples/
├── references/
└── scripts/
    ├── audit_figures.py
    ├── package_check.py
    ├── scimplstyle_mssp.py
    ├── scimplstyle_mssp_cli.py
    └── demos/
```

## Validation / 验证

Before publishing or sharing:

```bash
python scripts/package_check.py .
```

The package should contain only curated examples, references, and reusable scripts. Demo-generated outputs should stay outside the skill folder.
