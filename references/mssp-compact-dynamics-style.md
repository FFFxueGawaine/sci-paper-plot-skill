# MSSP Compact Dynamics Style Reference

This reference describes the generalized `MSSP Compact Dynamics` plotting style used by `scimplstyle_mssp`. It is intended for compact SCI manuscript figures in mechanical nonlinear dynamics, system identification, uncertainty quantification, and machine-learning-assisted modeling.

The style was distilled from a private paper figure set during development. Local paths, project identifiers, and private file names are intentionally omitted so the skill can be shared.

## Style Identity

- Style name: `MSSP Compact Dynamics`
- Python helper alias: `scimplstyle_mssp`
- Main use: compact, English-language SCI figures for mechanical nonlinear dynamics and ML-based model validation
- Default output: high-resolution `PNG`, `600 dpi`
- Optional output: `PDF` or `SVG` only when requested by a user or required by a journal

## Figure Families

| Family | Typical manuscript question | Style pattern | Template advice |
|---|---|---|---|
| Model validation / prediction comparison | Does the identified or learned model reproduce measured response? | black/blue experiment line, red identified/proposed line, optional confidence band or local zoom inset | standardize legend, use `time (s)`, keep line hierarchy clear |
| Local zoom / inset detail | What small difference appears near a peak, transient, or resonance region? | parent curve plus compact inset axes and thin connectors | use `add_zoom_inset()`, keep inset ticks small and inward, reserve blank parent-axes space, and avoid duplicate inset legends |
| Posterior distribution / KDE | Where are the posterior mass and uncertainty concentrated? | KDE or scatter density, colorbar, true/estimated markers, compact annotations | standardize colorbar, marker size, decimal precision, annotation placement |
| Physical relation / nonlinear stiffness | How does force, stiffness, or restoring relation vary with displacement? | one- or two-panel curve family, optional dashed components | keep formulas readable and avoid oversized annotations |
| Duffing / nonlinear system identification | Does the identified nonlinear model reproduce response and recover physical terms? | time validation, phase portrait, restoring force curve, coefficient bars | pair response validation with interpretable coefficients or library terms |
| Time-frequency / spectrogram | Where do transient frequency components appear in time? | top time response, bottom time-frequency energy map | use shared axis labeling and add colorbar only when it explains amplitude scale |
| FRF / frequency response | How do resonance peaks, damping, and nonlinear shifts compare? | blue/black/red curves, dB magnitude, frequency axis | use `fre. (Hz)` or `frequency (Hz)` consistently |
| Candidate library screening | Which terms or features dominate the discovered model? | stem or horizontal bar chart | double-column layout for many terms; shorten x labels if crowded |
| Mechanism schematic | What physical structure or states define the problem? | restrained colors, black structure lines, clear panel states | prefer editable vector only when the figure is a schematic |
| General line plot | How does a metric evolve with time, samples, noise, or parameter value? | one or more curves, optional markers, compact legend | use light grid only when it improves reading |
| General bar chart | Which method or case performs best on one metric? | categorical bars, compact value labels, light y-grid | avoid oversized category text and keep the baseline clear |
| Phase/Poincare plot | Does the response indicate periodic, quasi-periodic, or complex motion? | trajectory line plus sampled section points | use small points and compact double-column layout |
| Bifurcation diagram | How does response branch as excitation or system parameter changes? | dense parameter-response scatter | use tiny markers and avoid connecting branches with lines |
| Basin of attraction | Which initial conditions converge to different attractors? | classified initial-condition map | use restrained discrete colormap and compact colorbar |
| Error boxplot | How robust is each method over repeated trials? | boxplot, violin plot, or ECDF | emphasize median and distribution, not only the mean |

## Common Nonlinear Systems

Use these systems as common template anchors:

- Duffing: cubic stiffness; use time validation, phase portrait, restoring force, FRF/backbone, and parameter identification panels.
- Van der Pol: self-excited limit cycle; use phase portrait and amplitude-convergence panels.
- Nonlinear pendulum: sine restoring force and separatrix; use angle-phase and energy-like views.
- Bouc-Wen: hysteretic restoring force; use `force (N)` vs `dis. (mm)` loops and cyclic validation.
- Piecewise/freeplay oscillator: clearance or segmented stiffness; use event-marked time response, restoring force, bifurcation, and Poincare plots.

## Naming Pattern

Prefer concise names that express manuscript role:

- `Fig_validation_case1.png`
- `Fig_frf_comparison.png`
- `Fig_bifurcation_frequency.png`
- `Fig_ml_confusion_matrix.png`

For numbered manuscript figures, use consistent capitalization such as `Fig_01.png`, `Fig_02.png`, and so on.

## Common Corrections

- Prefer lowercase compact quantity labels: `dis.`, `vel.`, `acc.`, `amp.`, `mag.`, `err.`, `loss`.
- Keep official unit capitalization: use `fre. (Hz)`, `force (N)`, `stress (MPa)`, and `mag. (dB)` rather than lowercasing the unit symbols.
- Change `time(s)` to `time (s)`.
- Change `fre.(Hz)` to `fre. (Hz)` or `frequency (Hz)`.
- Change `dis.(mm)` to `dis. (mm)`.
- If a unit is unknown, omit it instead of using `(-)` as a placeholder; `format_axis_label(label, unit)` follows this rule.
- Do not add `(-)` to count or index axes such as `iteration`, `epoch`, `batch`, `sample index`, or `sample order`.
- Use `loss`, `f1 score`, and `auc` without `(-)` by default; reserve `(-)` for explicitly normalized physical quantities, coefficients, probabilities, density proxies, or energy-like measures.
- Keep panel labels bold and placed consistently; use `base_size + 4 pt` as the default template size.
- Keep legends in empty regions or outside axes when the plot is dense.
- Keep local zoom insets in empty regions; do not let the inset cover the very feature it is meant to explain.
- Widen the parent `ylim` when needed so the inset sits in blank space; use `bounds` for stable placement, hide connector lines that cross data, and use slightly larger save padding for inset figures.
- Keep grid lines light, behind data, and disabled on axes where they do not help reading.
- Keep layouts compact but leave enough spacing for x/y labels, titles, legends, colorbars, and panel labels. For dense `1 x 3` rows, add all labels/legends first and then call `apply_tight_layout(fig)` before saving.
- For regular `2 x 2` and `2 x 3` layouts, `constrained_layout=True` plus `set_panel_spacing(fig)` is usually sufficient. Inspect the rendered PNG and increase `w_pad`/`wspace` or switch to `apply_tight_layout(fig)` when y labels, colorbars, or legends sit between adjacent axes.
- Use consistent SNR colors if comparing `40 dB`, `30 dB`, and `20 dB`.
- Avoid large annotations on dense scatter or heatmap figures.

## Common Axis Labels

| Group | Preferred compact labels |
|---|---|
| Time and frequency | `time (s)`, `period (s)`, `fre. (Hz)`, `ang. fre. (rad/s)`, `phase (deg)` |
| Response | `dis. (mm)`, `vel. (mm/s)`, `acc. (m/s^2)`, `amp. (mm)`, `peak dis. (mm)`, `rms acc. (m/s^2)` |
| FRF and spectra | `mag. (dB)`, `phase (deg)`, `psd (dB/Hz)`, `energy (-)` |
| Mechanical properties | `force (N)`, `moment (N m)`, `torque (N m)`, `stiff. (N/mm)`, `damp. (N s/m)`, `mass (kg)` |
| Material or field quantities | `strain (-)`, `stress (MPa)`, `pressure (kPa)`, `temp. (K)` |
| Training progress | `iteration`, `epoch`, `batch`, `sample index`, `sample order`, `training samples` |
| Machine-learning metrics | `acc. (%)`, `err. (%)`, `rmse (mm)`, `mae (mm)`, `loss`, `f1 score`, `auc`, `train. time (s)`, `infer. time (ms)` |
