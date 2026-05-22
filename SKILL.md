---
name: sci-paper-plot-skill
description: This skill should be used when Codex needs publication-ready Matplotlib or Seaborn figures, SCI figure audits, reusable paper-figure templates, beginner-friendly plotting guidance, or MSSP Compact Dynamics style demos.
---

# Sci Paper Plot Skill

Style name: `MSSP Compact Dynamics`.

## Core Workflow

1. Inspect the target paper or project folder without editing original images or notebooks.
2. Run `scripts/audit_figures.py` when a figure inventory or notebook `savefig` trace is needed.
3. Classify figures by manuscript role, not by file extension. Read `references/mssp-compact-dynamics-style.md` for figure families and compact axis labels.
4. Recommend templates by user goal before explaining Matplotlib or Seaborn API details.
5. Use `scripts/scimplstyle_mssp.py` as the default plotting style module for new or regenerated figures.
6. Use `scripts/scimplstyle_mssp_cli.py` for helper commands such as `beginner-guide`, `run-brief`, `recommend`, `audit`, `preview-gallery`, and `check-demos`.
7. For figures that do not match a demo exactly, read `references/adaptation-guide.md` and adapt by figure intent, data geometry, and manuscript role.
8. Treat the skill folder as a template library; place user-specific plotting scripts and generated figures in the user's project workspace.

## Beginner And Pre-Run Rules

- If the user is a beginner, unsure how to start, does not know which plot type to choose, writes mainly in Chinese, or asks Codex to pick a template, read `references/codex-beginner-guide.zh-CN.md` and `README.zh-CN.md` first.
- Before running any operation that writes files, copies demos, generates figures, checks demo previews, or replaces placeholder data with real data, collect a short pre-run brief from the user.
- At minimum confirm the figure goal, data source, output folder outside the skill package, language/font choice, panel-label placement, and layout constraints.
- Read `references/pre-run-brief.zh-CN.md` or run `scripts/scimplstyle_mssp_cli.py run-brief --lang zh` for Chinese beginner users.
- Read-only commands such as `beginner-guide`, `recommend`, `list-demos`, and `style-guide` can be run without the pre-run brief.

## Workspace Boundaries

- Keep the installed skill folder and Git repository clean; do not use them as the normal place for user plot scripts or generated PNG/JPG/PDF/SVG files.
- When the user asks for a new plot script, create it under the user's current project/workspace, preferably in a run folder such as `plot_runs/<task-name>/`.
- When copying demo scripts, copy them to the run folder root so each demo writes figures to that run folder's `output/` directory.
- If the user does not specify a destination, choose a clear folder under the current working directory, then report the absolute script path and output path.
- Only write generated images inside the skill package when deliberately maintaining curated README examples under `assets/examples/`.
- Always open `.py`, `.txt`, and `.ipynb` with `encoding="utf-8"` when writing Python code.

## SCI Style Defaults

- Use Times New Roman for English text and Matplotlib mathtext with `mathtext.fontset = "stix"` for formulas.
- Allow SimSun (`宋体`) for Chinese report titles or Chinese-title figures.
- Export `PNG` at `600 dpi` by default; generate `PDF` or `SVG` only when explicitly requested by the user or journal.
- Use single-column width around `85 mm`; double-column width around `170-180 mm`.
- Use bold panel labels `(a)`, `(b)`, `(c)` consistently; default placement is above each axes: `panel_label(ax, "(a)")` / `loc="top-center"`.
- Use `loc="bottom-center"` only when the journal template or reference figure clearly puts panel labels below the axes.
- Write units with a space before parentheses: `time (s)`, `fre. (Hz)`, `dis. (mm)`, `mag. (dB)`.
- If a unit is unknown, omit the unit instead of writing `(-)`; use `format_axis_label(label, unit)` and reserve `(-)` for explicitly dimensionless quantities.
- Do not add `(-)` to count/index axes such as `iteration`, `epoch`, `batch`, `sample index`, or `sample order`; common ML metrics such as `loss`, `f1 score`, and `auc` also omit `(-)` by default.
- Keep labels, legends, line widths, markers, grid visibility, inset zooms, and colorbar placement consistent across the same figure family.
- Keep legends and grid lines secondary to data; use `safe_legend()` or an empty corner for legends, and place dense legends outside the axes.
- Keep layouts compact but never allow labels, titles, legends, colorbars, or panel labels to overlap between subplots; use `apply_tight_layout(fig)` after all labels/legends are created for dense multi-panel rows, or `constrained_layout=True` plus `set_panel_spacing(fig)` for regular layouts.
- Read `references/figure-quality-constraints.zh-CN.md` and `references/mssp-compact-dynamics-style.md` for the detailed style checklist.

## Style Levels

- Level 1: classify existing figures and record current risks.
- Level 2: create a reusable plotting style guide and Matplotlib style module.
- Level 3: only when explicitly requested, update notebooks or regenerate figures from data.

Default to Level 1 or Level 2 when the user asks to keep existing figures as a template.

## Resources

- `README.zh-CN.md`: Chinese-first quickstart for beginner users.
- `references/mssp-compact-dynamics-style.md`: figure families, style corrections, and compact axis labels.
- `references/codex-beginner-guide.zh-CN.md` and `references/codex-beginner-guide.en.md`: command-backed beginner guidance.
- `references/pre-run-brief.zh-CN.md` and `references/pre-run-brief.en.md`: pre-run prompt checklists.
- `references/figure-quality-constraints.zh-CN.md`: layout, language, title font, panel-label, unit, and export constraints.
- `references/common-plot-types-catalog.md` and `references/plot-type-map.zh-CN.md`: common plot-type lookup tables.
- `references/demo-index.json`: machine-readable demo metadata used by `recommend`, `preview-gallery`, and `check-demos`.
- `references/hb-clearance-paper-figure-templates.md`: figure-by-figure map for the built-in MSSP clearance-system paper.
- `scripts/scimplstyle_mssp.py`: importable Matplotlib helper module.
- `scripts/scimplstyle_mssp_cli.py`: beginner-friendly command entry point.
- `scripts/demos/`: runnable Matplotlib and Seaborn demos.

## Example Commands

```powershell
python scripts/scimplstyle_mssp_cli.py beginner-guide --lang zh
python scripts/scimplstyle_mssp_cli.py run-brief --lang zh
python scripts/scimplstyle_mssp_cli.py recommend "误差分布" --lang zh
python scripts/scimplstyle_mssp_cli.py list-demos
python scripts/audit_figures.py "<paper-figure-folder>" --markdown
python scripts/package_check.py .
```

## Dependencies

- Python 3.9 or later.
- Runtime packages: `numpy`, `matplotlib`, `pandas`, `seaborn`, and `Pillow`.
- Validation package: `PyYAML`, used by external skill validation helpers.
- Install with `python -m pip install -r requirements.txt` from the skill directory.
