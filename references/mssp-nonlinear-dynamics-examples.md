# MSSP-Style Nonlinear Dynamics Figure Examples

These examples are synthetic templates for mechanical nonlinear dynamics papers, not benchmark data.

## Common Figure Types

| Figure type | Typical manuscript question | Template file |
|---|---|---|
| Duffing analysis and identification | Does the identified cubic-stiffness model reproduce the measured response and restoring force? | `demo_duffing_identification.py` |
| Local zoom validation detail | Where do small response errors appear in the validation curve? | `demo_validation_inset_zoom.py` |
| Common nonlinear systems gallery | Which nonlinear behavior family is being illustrated or compared? | `demo_nonlinear_systems_gallery.py` |
| Sparse nonlinear library identification | Which candidate terms are retained and how small is the validation residual? | `demo_nonlinear_identification_library.py` |
| Phase portrait + Poincare section | Does the response settle to periodic, quasi-periodic, or complex motion? | `demo_phase_poincare.py` |
| Bifurcation diagram | How does the response branch as excitation frequency or amplitude changes? | `demo_bifurcation_diagram.py` |
| Time response + time-frequency map | Where do transient frequency components appear in time? | `demo_time_frequency_map.py` |
| Basin of attraction | Which initial conditions converge to different attractors? | `demo_basin_attraction.py` |
| Error boxplot | How robust is each identification or prediction method over repeated trials? | `demo_error_boxplot.py` |

## System-Specific Advice

| System | Typical equation or feature | Recommended plots |
|---|---|---|
| Duffing oscillator | cubic stiffness, hardening or softening response | time validation, phase portrait, restoring force `force (N)` vs `dis. (mm)`, FRF/backbone, coefficient bar chart |
| Van der Pol oscillator | self-excited damping and limit cycle | phase portrait, amplitude convergence, parameter sweep over `mu` |
| Nonlinear pendulum | large-angle sine restoring force and separatrix | phase portrait, energy-like contour, period-amplitude curve |
| Bouc-Wen hysteresis | rate-dependent hysteretic restoring force | `force (N)` vs `dis. (mm)` loop, cyclic validation, parameter comparison |
| Piecewise or freeplay oscillator | clearance, dead-zone, or segmented stiffness | restoring force curve, event-marked time response, bifurcation, Poincare section |

For identification papers, pair at least one response-validation plot with one parameter or candidate-library plot. This makes it clear whether the method both predicts the response and recovers interpretable physics.

## Style Notes

- Use double-column width for dense phase/Poincare and time-frequency composites.
- Use single-column width for one-panel bifurcation, basin, boxplot, and bar chart figures.
- For dense scatter plots, reduce marker size before increasing figure size.
- For color maps, keep labels and colorbar compact; avoid decorative colormaps unless the physics requires them.
- For categorical method comparison, use restrained colors and black edges.
- For Duffing and restoring-force plots, keep `dis. (mm)`, `vel. (mm/s)`, `force (N)`, and `coef. value` labels consistent across panels.
