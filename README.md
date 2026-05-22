# Sci Paper Plot Skill

Reusable Codex skill for turning SCI paper figures into classified, reusable Matplotlib and Seaborn templates.

中文用户请优先阅读 `README.zh-CN.md`。

## What It Solves

This skill helps with a recurring paper-figure problem: figures are scattered across notebooks, styles drift between panels, and good reference-paper plots are hard to reuse. The workflow is:

1. Audit existing figures and notebook `savefig` calls.
2. Classify figures by manuscript role, not by file extension.
3. Recommend or copy a runnable demo.
4. Replace placeholder arrays with real project data outside the skill folder.

## Core Ideas

- Classify by manuscript role: validation, uncertainty, FRF, time-frequency, candidate-library selection, schematic, etc.
- Keep style and scientific meaning together: axis semantics, units, panel labels, density meaning, and validation hierarchy.
- Omit unknown and dimensionless units; do not use `(-)` unless the user or journal explicitly requires it.
- Use synthetic demo data in the skill package; keep private paper data and generated figures in the user workspace.
- Let the skill improve by adding paper maps, demo metadata, and package checks after each curated reference paper.

## Built-In Reference Paper

- Yusheng Wang, Hui Qian, Qinghua Liu, Yinhang Ma, Dong Jiang. **Hierarchical Bayesian model for identifying clearance-type nonlinear system**. *Mechanical Systems and Signal Processing*, 235, 112891, 2025.
- DOI: [10.1016/j.ymssp.2025.112891](https://doi.org/10.1016/j.ymssp.2025.112891)

Paper-specific resources:

- `references/hb-clearance-paper-figure-templates.md`
- `scripts/demos/demo_hb_clearance_templates.py`
- `scripts/demos/demo_hb_fig14_three_column.py`

## Install

```bash
git clone https://github.com/FFFxueGawaine/sci-paper-plot-skill.git ~/.codex/skills/sci-paper-plot-skill
cd ~/.codex/skills/sci-paper-plot-skill
python -m pip install -r requirements.txt
```

Update later with:

```bash
cd ~/.codex/skills/sci-paper-plot-skill
git pull
```

## Quick Use

```bash
python scripts/scimplstyle_mssp_cli.py beginner-guide --lang zh
python scripts/scimplstyle_mssp_cli.py run-brief --lang zh
python scripts/scimplstyle_mssp_cli.py recommend "误差分布" --lang zh
python scripts/scimplstyle_mssp_cli.py list-demos
python scripts/audit_figures.py "path/to/paper/figures" --markdown
```

Commands that generate or copy files should target a working folder outside this skill package:

```bash
python scripts/scimplstyle_mssp_cli.py copy-demos paper-plot-workspace
python scripts/scimplstyle_mssp_cli.py preview-gallery paper-plot-preview --set curated
python scripts/scimplstyle_mssp_cli.py check-demos paper-plot-preview --set curated
```

## Main References

- `README.zh-CN.md`: Chinese-first quickstart.
- `references/codex-beginner-guide.zh-CN.md`: Chinese beginner route.
- `references/pre-run-brief.zh-CN.md`: questions to ask before file-writing plot operations.
- `references/mssp-compact-dynamics-style.md`: figure families, style corrections, and compact axis labels.
- `references/figure-quality-constraints.zh-CN.md`: layout, language, title font, panel-label, and export constraints.
- `references/common-plot-types-catalog.md`: common Matplotlib and Seaborn plot types.
- `references/plot-type-map.zh-CN.md`: Chinese plot-name to API/demo mapping.
- `references/demo-index.json`: machine-readable demo index used by `recommend`, `preview-gallery`, and `check-demos`.

## Self-Learning Loop

When adding a new reference paper:

1. Run `scripts/audit_figures.py` on the paper figure folder.
2. Add a figure-template map under `references/`.
3. Add runnable demos under `scripts/demos/` using synthetic placeholder data.
4. Register demo metadata in `references/demo-index.json`.
5. Run `python scripts/package_check.py .`.

## Validation

```bash
python scripts/package_check.py .
```

The package should contain only curated examples, references, and reusable scripts. Demo-generated outputs should stay outside the skill folder.
