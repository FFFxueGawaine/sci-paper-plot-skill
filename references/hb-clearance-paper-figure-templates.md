# Hierarchical Bayesian Clearance Paper Figure Templates

This reference maps the figures from the paper below to reusable plotting templates in this skill. It is a style-and-template guide, not an official figure-caption source.

Reference paper:

- Title: Hierarchical Bayesian model for identifying clearance-type nonlinear system
- Journal: Mechanical Systems and Signal Processing, Volume 235, 15 July 2025, Article 112891
- DOI: https://doi.org/10.1016/j.ymssp.2025.112891
- ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S0888327025005928

The local authoring archive used for the template pass contains exported figures named `Fig.004` through `Fig.018`, plus several working figures. Source paths in this document are intentionally relative to that archive root so the skill package does not store private machine paths.

## Use Levels

| Level | Use when | What to do | Benefit |
|---|---|---|---|
| Level 1 | The user only wants a style checklist | Read the table below and classify the target figure role | Fast, low risk, does not touch original notebooks |
| Level 2 | The user wants a reusable drawing template | Run `scripts/demos/demo_hb_clearance_templates.py` and adapt the closest generated template | Gives a working Matplotlib starting point for every paper figure |
| Level 3 | The user wants to regenerate manuscript figures | Replace placeholder arrays in the demo with real variables from the source notebooks | Keeps the published style while making the figure reproducible |

Run all templates:

```bash
python scripts/demos/demo_hb_clearance_templates.py
```

The script writes placeholder template images to `scripts/demos/output/hb_clearance_templates/` when run in place, or to the copied demo folder's `output/hb_clearance_templates/` when copied to a project workspace.

## Figure Template Map

| Figure | Skill taxonomy category | Manuscript role | Source family | Template function | Template output | Style notes |
|---|---|---|---|---|---|---|
| Fig. 1 | Bayesian workflow / method-flow schematic | Probabilistic identification workflow | Method schematic | `template_fig001_bayesian_workflow` | `Fig.001_bayesian_workflow_template.png` | Use a clean left-to-right flow: response data, candidate library, sparse prior, posterior model, validation. |
| Fig. 2 | Clearance basis / piecewise contact relation | Clearance basis and segmented model selection | Method schematic | `template_fig002_clearance_basis` | `Fig.002_clearance_basis_template.png` | Show negative gap, free zone, positive gap, and active Heaviside segments with consistent colors. |
| Fig. 3 | Model structure / mechanism schematic | One-sided impact oscillator schematic | Method schematic | `template_fig003_one_sided_impact` | `Fig.003_one_sided_impact_template.png` | Use simple mechanics glyphs; label mass, spring, damper, stop, and clearance without dense text. |
| Fig. 4 | Posterior predictive check / marginal posterior density | Posterior predictive KDE comparison for Case 1 | `case1/main_1.ipynb` | `template_fig004_ppc_kde` | `Fig.004_ppc_kde_template.png` | Three KDE panels, experiment in black, posterior samples in restrained colors, compact `R^2` annotation. |
| Fig. 5 | Candidate-library selection / sparse-term probability | Candidate library selection under SNR levels | `case1/plot.ipynb` | `template_fig005_library_selection` | `Fig.005_library_selection_template.png` | Wide library stem plot; use dashed decision threshold and shaded model groups. |
| Fig. 6 | Posterior predictive check / marginal posterior density | Marginal posterior densities for selected parameters | `case1/plot.ipynb` | `template_fig006_posterior_density_grid` | `Fig.006_posterior_density_grid_template.png` | Six compact density panels with true/mean markers and uncertainty bands. |
| Fig. 7 | Experimental setup / rig schematic or photo redraw | Tri-stable NES mechanism schematic | Schematic or external model drawing | `template_fig007_tristable_nes_schematic` | `Fig.007_tristable_nes_schematic_template.png` | Keep as vector-style schematic; use blue/red magnets and black mechanical frame. |
| Fig. 8 | Clearance basis / piecewise contact relation | Piecewise restoring-force relation | `case2/Fig.8.ipynb` | `template_fig008_piecewise_force` | `Fig.008_piecewise_force_template.png` | Two panels: measured or target force curve, then basis-component decomposition. |
| Fig. 9 | Candidate-library selection / sparse-term probability | Candidate library selection for tri-stable system | `case2/plot.ipynb` | `template_fig009_library_selection_tristable` | `Fig.009_library_selection_tristable_template.png` | Similar to Fig. 5 but fewer active terms; keep active stems visually dominant. |
| Fig. 10 | Posterior predictive check / marginal posterior density | Posterior density triplet for tri-stable parameters | `case2/plot.ipynb` | `template_fig010_density_triplet` | `Fig.010_density_triplet_template.png` | Three horizontal panels; align y label `density` and keep annotations inside empty regions. |
| Fig. 11 | Joint posterior scatter / parameter uncertainty map | Joint posterior scatter or density panels | `case2/plot.ipynb` | `template_fig011_joint_posterior_scatter` | `Fig.011_joint_posterior_scatter_template.png` | Four scatter-density panels with small markers, alpha, and colorbar. |
| Fig. 12 | Model validation / prediction comparison | Prediction or validation time history for Case 2 | `case2/predict.ipynb` | `template_fig012_validation_timeseries` | `Fig.012_validation_timeseries_template.png` | Three panels; experiment/reference in black, identified/proposed in red dashed, uncertainty as light band. |
| Fig. 13 | Experimental setup / rig schematic or photo redraw | Experimental rig or cantilever-clearance setup | Photo or schematic | `template_fig013_experimental_setup` | `Fig.013_experimental_setup_template.png` | Use a schematic redraw template when the original is a photo; annotate sensor, beam, stops, and clearance. |
| Fig. 14 | Time-frequency / spectrogram | Experimental time response and time-frequency map | `case3/Fig14-15.ipynb` | `template_fig014_time_frequency_composite`; top-row demo: `demo_hb_fig14_three_column.py` | `Fig.014_time_frequency_composite_template.png`; demo output: `demo_hb_fig14_three_column.png` | Pair time responses with spectrogram panels; when only the top response row is needed, use the one-row three-column demo. |
| Fig. 15 | Posterior predictive check / marginal posterior density | Experimental displacement and clearance-density estimate | `case3/Fig14-15.ipynb` | `template_fig015_time_hist_clearance` | `Fig.015_time_hist_clearance_template.png` | Two-panel layout: time trace plus density/histogram; mark estimated clearances with vertical lines. |
| Fig. 16 | Joint posterior scatter / parameter uncertainty map | Experimental joint posterior scatter panels | `case3/plotnonlinear.ipynb` | `template_fig016_experimental_joint_posterior` | `Fig.016_experimental_joint_posterior_template.png` | Four panels; preserve parameter-pair meaning and use shared colorbar semantics. |
| Fig. 17 | Multi-response validation / force-phase validation | Experimental multi-response validation | `case3/main_est copy.ipynb` | `template_fig017_multidof_validation` | `Fig.017_multidof_validation_template.png` | Four time-history panels with local inset zoom; show testing/training intervals if relevant. |
| Fig. 18 | Multi-response validation / force-phase validation | Identified force validation and phase portrait | `case3/main_est copy.ipynb` | `template_fig018_force_phase_validation` | `Fig.018_force_phase_validation_template.png` | Put force validation first and phase portrait second; use inset only for waveform detail. |

## Classification Groups

| Skill taxonomy category | Paper figures | Template family |
|---|---|---|
| Bayesian workflow / method-flow schematic | Fig. 1 | workflow box diagram |
| Model structure / mechanism schematic | Fig. 3 | one-sided impact schematic |
| Experimental setup / rig schematic or photo redraw | Fig. 7, Fig. 13 | tri-stable NES and cantilever setup schematic |
| Clearance basis / piecewise contact relation | Fig. 2, Fig. 8 | clearance basis and piecewise restoring force |
| Posterior predictive check / marginal posterior density | Fig. 4, Fig. 6, Fig. 10, Fig. 15 | KDE, marginal posterior, clearance-density estimate |
| Candidate-library selection / sparse-term probability | Fig. 5, Fig. 9 | stem probability and active-term screening |
| Joint posterior scatter / parameter uncertainty map | Fig. 11, Fig. 16 | scatter-density parameter uncertainty map |
| Model validation / prediction comparison | Fig. 12 | time-domain prediction validation |
| Time-frequency / spectrogram | Fig. 14 | response plus spectrogram composite |
| Multi-response validation / force-phase validation | Fig. 17, Fig. 18 | multi-DOF validation, force trace, and phase portrait |

## Extra Working Figures

| Working figure | Source family | Recommended handling |
|---|---|---|
| `Fig.000_frf` and `fig.frfest` | `case3/mat/fig_frf.ipynb`, MATLAB FRF estimate | Use the existing FRF template family: `demo_frf_compare.py`; keep `fre. (Hz)` and `mag. (dB)`. |
| `inverse_gamma_shapes` | `case1/invgama.ipynb` | Treat as a prior-sensitivity grid; reuse Fig. 6 density-grid rules but mark it as a method appendix figure. |

## Adaptation Checklist

- Keep one figure number per output stem, for example `Fig.012_validation_timeseries`.
- Convert notebook-level font dictionaries into `apply_sci_style()` plus `panel_label()`.
- Use `save_figure(fig, stem, out_dir=...)` instead of raw `plt.savefig(...)`.
- Preserve statistical meaning: posterior predictive KDE, marginal posterior density, joint posterior scatter, and validation uncertainty bands are not interchangeable.
- For schematic figures, prefer clean vector redraws rather than bitmap screenshots when the manuscript needs editable graphics.
- When replacing placeholders with real arrays, keep the figure geometry first; change data second; only then tune axis limits and annotations.
