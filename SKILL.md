---
name: sci-paper-plot-skill
description: Create and apply reusable SCI paper plotting templates with the MSSP Compact Dynamics / scimplstyle_mssp Matplotlib style. Use when Codex needs publication-ready Matplotlib figures, SCI manuscript plot style guidance, mechanical nonlinear dynamics figures, system identification plots, uncertainty visualization, machine-learning result plots, exported .jpg/.png/.tif figure audits, Jupyter notebook savefig tracing, or English SCI paper figure templates without modifying existing figures.
---

# Sci Paper Plot Skill

Style name: `MSSP Compact Dynamics`.

## Core Workflow

1. Inspect the target paper directory without editing original images or notebooks.
2. Run `scripts/audit_figures.py` when a figure inventory is needed.
3. Classify figures by manuscript role, not by file extension.
4. Preserve the existing visual intent as a style reference; only propose regenerated templates when requested.
5. Use `scripts/scimplstyle_mssp.py` as the default Matplotlib style module for new or regenerated figures.
6. Use `scripts/scimplstyle_mssp_cli.py` when the user wants subcommands such as `audit`, `style-guide`, or demo scaffolds.
7. For figures that do not match a demo exactly, read `references/adaptation-guide.md` and adapt by figure intent, data geometry, and manuscript role.
8. Treat the skill folder as a template library; place user-specific plotting scripts and generated figures in the user's project workspace.

Always open `.py`, `.txt`, and `.ipynb` with `encoding="utf-8"` when writing Python code. Treat terminal mojibake as display-only; inspect bytes/files with UTF-8 aware tools before calling text corrupted.

## Workspace Usage

- Keep the installed skill folder and Git repository clean; do not use them as the normal place for user plot scripts or generated PNG/JPG/PDF/SVG files.
- When the user asks for a new plot script, create it under the user's current project/workspace, preferably in a run folder such as `plot_runs/<task-name>/`.
- When copying demo scripts, copy them to the run folder root so each demo writes figures to that run folder's `output/` directory.
- If the user does not specify a destination, choose a clear folder under the current working directory, then report the absolute script path and output path.
- Only write generated images inside the skill package when deliberately maintaining curated README examples under `assets/examples/`.

## Figure Taxonomy

Use these categories for paper figure inventories:

- Model structure / mechanism schematic
- Nonlinear stiffness or physical relation curve
- Time-domain response
- Frequency response / FRF
- Time-frequency / spectrogram
- Posterior distribution / KDE / uncertainty
- Model validation / prediction comparison
- Exploratory prior or candidate-library screening

For each exported figure, collect:

- Absolute path
- Case or experiment folder
- Figure type
- Manuscript purpose
- Source notebook and `savefig` target if discoverable
- Format, pixels, DPI
- Current style
- Main style risks
- Recommended reusable export format
- Revision priority

## SCI Style Defaults

- Use Times New Roman for English text.
- Use Matplotlib mathtext with `mathtext.fontset = "stix"` for formulas.
- For these demos, export `PNG` at `600 dpi` by default; generate `PDF` or `SVG` only when explicitly requested by the user or journal.
- Use single-column width around `85 mm`; double-column width around `170-180 mm`.
- Use bold panel labels `(a)`, `(b)`, `(c)` consistently; default to `base_size + 4 pt`, e.g. `14 pt` when base text is `10 pt`.
- Write units with a space before parentheses: `time (s)`, `fre. (Hz)`, `dis. (mm)`, `mag. (dB)`.
- Keep labels, legends, line widths, markers, grid visibility, and colorbar placement consistent across the same figure family.
- Keep legends and grid lines secondary to data: use `safe_legend()` or an empty corner for legends, place dense legends outside the axes, and keep grid lines light, behind plotted data, and never visually dominant.
- Keep layouts compact but never crop axis labels; use `constrained_layout=True`, small `labelpad`, and save with a safety `pad_inches` around `0.04`.
- Avoid using JPEG as the only master format for generated plots; JPEG is acceptable only as a preview copy.

## Style Levels

- Level 1: classify existing figures and record current risks.
- Level 2: create a reusable plotting style guide and Matplotlib style module.
- Level 3: only when explicitly requested, update notebooks or regenerate figures from data.

Default to Level 1 or Level 2 when the user asks to keep existing figures as a template.

## Dependencies

- Python 3.9 or later.
- Runtime packages: `numpy`, `matplotlib`, and `Pillow`.
- Validation package: `PyYAML`, used by external skill validation helpers.
- Install with `python -m pip install -r requirements.txt` from the skill directory.

## Resources

- `references/mssp-compact-dynamics-style.md`: generalized style reference for the MSSP Compact Dynamics plotting style.
- `references/adaptation-guide.md`: rules for adapting arbitrary plotting code or existing images into the style without forcing exact demo shapes.
- `references/mssp-nonlinear-dynamics-examples.md`: MSSP-style nonlinear dynamics figure examples and their demo files.
- `references/machine-learning-figure-examples.md`: machine-learning figure examples such as radar charts, confusion matrices, residual plots, feature importance, and hyperparameter heatmaps.
- `references/matplotlib-gallery-examples.md`: broader gallery examples for common Matplotlib plot families in SCI-style manuscripts.
- `scripts/audit_figures.py`: read-only inventory for exported images and notebook `savefig` calls.
- `scripts/scimplstyle_mssp.py`: importable Matplotlib helper module for future SCI-style figures.
- `scripts/scimplstyle_mssp_cli.py`: beginner-friendly command entry point with subcommands.
- `scripts/package_check.py`: lightweight pre-package validation without PyYAML.
- `scripts/demos/`: runnable Matplotlib demos for validation comparison, uncertainty scatter, FRF comparison, line plot, bar chart, phase/Poincare, bifurcation, time-frequency, basin, boxplot, common machine-learning figures, and broader Matplotlib gallery figures.
- `requirements.txt`: runtime dependencies for demos and audit scripts.

Example use:

```powershell
python scripts/audit_figures.py "<paper-figure-folder>" --markdown
python scripts/scimplstyle_mssp_cli.py style-guide
python scripts/scimplstyle_mssp_cli.py list-demos
python scripts/scimplstyle_mssp_cli.py copy-demos "<demo-output-folder>"
```

Example plotting import:

```python
from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, save_figure

apply_sci_style()
fig, ax = plt.subplots(figsize=figure_size("double", 0.42))
panel_label(ax, "(a)")
save_figure(fig, "Fig.001", out_dir="figures")
```
