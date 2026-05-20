# scimplstyle_mssp Adaptation Guide

Use this guide when the user's code or image is not identical to the demos. The goal is style transfer, not cloning.

## Decision Order

1. Identify the figure's manuscript role:
   validation, line trend, FRF, uncertainty, time-frequency, histogram/KDE, mechanism schematic, or screening plot.
2. Preserve the scientific meaning:
   keep original variables, units, scale type, ordering, and statistical meaning unless the user asks to revise them.
3. Apply shared style rules:
   Times New Roman, STIX math, compact layout, no cropped labels, consistent panel labels, 600 dpi bitmap plus vector master.
4. Choose the closest template only as a starting point:
   a line chart can borrow colors from validation plots; a scatter plot can borrow colorbar/marker rules from uncertainty plots.
5. Adjust layout to the real data:
   single panel, multi-panel, wide panel, colorbar, inset, or legend placement should follow the data, not the demo.

## Mapping From Existing Code To Style

| If code contains | Likely figure type | Adaptation rule |
|---|---|---|
| `plt.plot`, `ax.plot` with 1-3 curves | line plot or validation plot | use compact line widths, clear legend, optional markers only when sampling points matter |
| zoomed region, `inset_axes`, or peak-detail comparison | local zoom inset | use `add_zoom_inset()`; keep tick labels small, avoid duplicate legends inside the inset, and mark the zoomed region with thin connectors |
| `plt.scatter`, `ax.scatter` | scatter/uncertainty plot | use small markers, alpha, colorbar only if color encodes a variable |
| `plt.bar`, `ax.bar`, `barh` | comparison bar chart | use compact value labels, one clear y metric, and light y-axis grid |
| `hist`, `kdeplot`, `az.plot_posterior` | posterior/KDE plot | standardize density labels, decimal precision, and annotation placement |
| `imshow`, `pcolormesh`, `specgram`, `spectrogram` | time-frequency or basin plot | preserve colormap semantics; add colorbar only when useful |
| `boxplot`, `violinplot` | repeated-trial error comparison | keep categories compact, use restrained fills, and emphasize medians |
| dense parameter-response scatter | bifurcation diagram | use very small markers, no connecting lines, and enough axis margin |
| semilog or dB magnitude labels | FRF/frequency response | use `fre. (Hz)` or `frequency (Hz)`, `mag. (dB)`, and blue/black/red line hierarchy |
| many categorical x labels | screening/library plot | prefer double-column width; rotate or shorten labels; avoid oversized markers |

## Layout Rules For Non-Demo Figures

- Use `constrained_layout=True` by default.
- Use `save_figure(..., pad_inches=0.04)` unless labels are still at risk; then increase to `0.06`.
- For single-column figures, start with `figure_size("single", 0.60-0.75)`.
- For double-column figures, start with `figure_size("double", 0.38-0.48)`.
- Put y labels only on the left side when subplots share the same y meaning.
- Keep x/y label `labelpad` small, usually `2`.
- Use legends inside the plot only when they do not cover important data; otherwise place outside or above.
- Use local zoom insets only when they reveal a real detail; place them in an empty region and avoid covering peaks, dense scatter, or legends.
- For dense plots, reduce marker size before increasing figure size.

## Code Adaptation Checklist

- Keep file writing UTF-8 if creating `.py`, `.txt`, or `.ipynb`.
- Replace raw `plt.savefig(...)` with `save_figure(fig, "Fig.xxx", out_dir=...)`.
- Call `apply_sci_style(base_size=8)` for compact single-column figures.
- Call `apply_sci_style(base_size=10)` for larger double-column or presentation-like figures.
- Add `panel_label(ax, "(a)")` for manuscript panels.
- Use `add_zoom_inset(ax, xlim=(...), ylim=(...))` for local magnified views instead of manually placing a large extra panel when the detail is small.
- Use units with spaces: `time (s)`, `fre. (Hz)`, `dis. (mm)`.
- Prefer lowercase compact quantity labels such as `vel.`, `acc.`, `amp.`, `mag.`, `err.`, `rmse`, and `loss`.
- Keep official unit capitalization: `Hz`, `N`, `MPa`, and `dB` should not be forced to lowercase.
- Verify by opening the generated PNG, not only by trusting the terminal.
