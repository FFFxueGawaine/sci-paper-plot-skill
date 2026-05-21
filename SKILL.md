---
name: sci-paper-plot-skill
description: Create and apply reusable SCI paper plotting templates with the MSSP Compact Dynamics / scimplstyle_mssp Matplotlib style. Use when Codex needs publication-ready Matplotlib or Seaborn figures, SCI manuscript plot style guidance, beginner-friendly Codex plotting guidance, mechanical nonlinear dynamics figures, clearance-type nonlinear system figures, system identification plots, uncertainty visualization, machine-learning result plots, exported .jpg/.png/.tif figure audits, Jupyter notebook savefig tracing, or English SCI paper figure templates without modifying existing figures.
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

If the user says they are a beginner, first-time user, unsure how to start, do not know which plot type to choose, writes mainly in Chinese, or asks Codex to help pick a template, read `references/codex-beginner-guide.md` and, for Chinese users, `README.zh-CN.md` plus `references/plot-type-map.zh-CN.md` first. Guide them through Level 1, Level 2, or Level 3, and recommend a template by user goal before explaining Matplotlib or Seaborn API details.

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
- Bayesian workflow / method-flow schematic
- Experimental setup / rig schematic or photo redraw
- Nonlinear stiffness or physical relation curve
- Clearance basis / piecewise contact relation
- Duffing / Van der Pol / pendulum / Bouc-Wen nonlinear system analysis
- Time-domain response
- Local zoom / inset validation detail
- Frequency response / FRF
- Time-frequency / spectrogram
- Posterior distribution / KDE / uncertainty
- Posterior predictive check / marginal posterior density
- Joint posterior scatter / parameter uncertainty map
- Model validation / prediction comparison
- Multi-response validation / force-phase validation
- Nonlinear system identification / sparse candidate-library coefficients
- Candidate-library selection / sparse-term probability
- Exploratory prior or candidate-library screening
- Clearance-type nonlinear system / hierarchical Bayesian identification template

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
- Prefer lowercase compact quantity labels such as `dis.`, `vel.`, `acc.`, `amp.`, `mag.`, `err.`, and `loss`; keep official unit capitalization such as `Hz`, `N`, `MPa`, and `dB`.
- Keep labels, legends, line widths, markers, grid visibility, inset zooms, and colorbar placement consistent across the same figure family.
- Keep legends and grid lines secondary to data: use `safe_legend()` or an empty corner for legends, place dense legends outside the axes, and keep grid lines light, behind plotted data, and never visually dominant.
- Keep layouts compact but never crop axis labels; use `constrained_layout=True`, small `labelpad`, and save with a safety `pad_inches` around `0.04`.
- Use local zoom insets when a validation, FRF, or peak-region figure needs to show small differences without losing the full trend; reserve blank space in the parent axes, use `bounds` for deterministic placement, hide any connector that crosses data, and save with extra padding.
- Avoid using JPEG as the only master format for generated plots; JPEG is acceptable only as a preview copy.

## Axis Label Conventions

Use these common labels as the default compact style:

- Time and frequency: `time (s)`, `period (s)`, `fre. (Hz)`, `ang. fre. (rad/s)`, `phase (deg)`.
- Response: `dis. (mm)`, `vel. (mm/s)`, `acc. (m/s^2)`, `amp. (mm)`, `peak dis. (mm)`, `rms acc. (m/s^2)`.
- FRF and spectra: `mag. (dB)`, `phase (deg)`, `psd (dB/Hz)`, `energy (-)`.
- Mechanical properties: `force (N)`, `moment (N m)`, `torque (N m)`, `stiff. (N/mm)`, `damp. (N s/m)`, `mass (kg)`.
- Material or field quantities: `strain (-)`, `stress (MPa)`, `pressure (kPa)`, `temp. (K)`.
- Machine-learning metrics: `acc. (%)`, `err. (%)`, `rmse (mm)`, `mae (mm)`, `loss (-)`, `f1 score (-)`, `auc (-)`, `train. time (s)`, `infer. time (ms)`.

## Style Levels

- Level 1: classify existing figures and record current risks.
- Level 2: create a reusable plotting style guide and Matplotlib style module.
- Level 3: only when explicitly requested, update notebooks or regenerate figures from data.

Default to Level 1 or Level 2 when the user asks to keep existing figures as a template.

## Dependencies

- Python 3.9 or later.
- Runtime packages: `numpy`, `matplotlib`, `pandas`, `seaborn`, and `Pillow`.
- Validation package: `PyYAML`, used by external skill validation helpers.
- Install with `python -m pip install -r requirements.txt` from the skill directory.

## Resources

- `references/mssp-compact-dynamics-style.md`: generalized style reference for the MSSP Compact Dynamics plotting style.
- `README.zh-CN.md`: Chinese-first quickstart for beginner users.
- `references/codex-beginner-guide.md`: beginner-friendly Codex usage guide with levels, prompts, and common workflows.
- `references/adaptation-guide.md`: rules for adapting arbitrary plotting code or existing images into the style without forcing exact demo shapes.
- `references/mssp-nonlinear-dynamics-examples.md`: MSSP-style nonlinear dynamics figure examples, including Duffing, Van der Pol, pendulum, Bouc-Wen, and nonlinear identification demo files.
- `references/hb-clearance-paper-figure-templates.md`: figure-by-figure template map for the hierarchical Bayesian clearance-type nonlinear system paper.
- `references/machine-learning-figure-examples.md`: machine-learning figure examples such as radar charts, confusion matrices, residual plots, feature importance, and hyperparameter heatmaps.
- `references/matplotlib-gallery-examples.md`: broader gallery examples for common Matplotlib plot families in SCI-style manuscripts.
- `references/common-plot-types-catalog.md`: compact lookup table for common Matplotlib and Seaborn plot types and their manuscript uses.
- `references/plot-type-map.zh-CN.md`: Chinese plot type lookup table mapping user wording to Matplotlib/Seaborn APIs and demos.
- `references/demo-index.json`: machine-readable demo metadata used by `recommend`, `preview-gallery`, and `check-demos`.
- `scripts/audit_figures.py`: read-only inventory for exported images and notebook `savefig` calls.
- `scripts/scimplstyle_mssp.py`: importable Matplotlib helper module for future SCI-style figures, including `add_zoom_inset()` for local magnified panels.
- `scripts/scimplstyle_mssp_cli.py`: beginner-friendly command entry point with subcommands, including `beginner-guide` for template selection.
- `scripts/package_check.py`: lightweight pre-package validation without PyYAML.
- `scripts/demos/`: runnable Matplotlib and Seaborn demos for validation comparison, local zoom inset, uncertainty scatter, FRF comparison, line plot, bar chart, Duffing identification, common nonlinear systems, sparse nonlinear library identification, hierarchical Bayesian clearance-system figures, phase/Poincare, bifurcation, time-frequency, basin, boxplot, common machine-learning figures, broader Matplotlib gallery figures, and common Seaborn `DataFrame` plot types.
- `requirements.txt`: runtime dependencies for demos and audit scripts.

Example use:

```powershell
python scripts/audit_figures.py "<paper-figure-folder>" --markdown
python scripts/scimplstyle_mssp_cli.py beginner-guide --lang zh
python scripts/scimplstyle_mssp_cli.py recommend "误差分布" --lang zh
python scripts/scimplstyle_mssp_cli.py list-demos
python scripts/scimplstyle_mssp_cli.py style-guide
python scripts/scimplstyle_mssp_cli.py copy-demos "<demo-output-folder>"
python scripts/scimplstyle_mssp_cli.py preview-gallery "<preview-output-folder>" --set curated
python scripts/scimplstyle_mssp_cli.py check-demos "<preview-output-folder>" --set curated
```

Example plotting import:

```python
from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, save_figure

apply_sci_style()
fig, ax = plt.subplots(figsize=figure_size("double", 0.42))
panel_label(ax, "(a)")
save_figure(fig, "Fig.001", out_dir="figures")
```
