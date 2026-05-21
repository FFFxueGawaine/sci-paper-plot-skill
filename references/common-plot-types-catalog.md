# Common Plot Types Catalog

This catalog maps common Matplotlib and Seaborn plot types to reusable SCI-style demo families in this skill.

## Current Coverage Summary

| Library | Plot family | Plot types covered | Demo file |
|---|---|---|---|
| Matplotlib | Relationship and uncertainty | line, confidence band, errorbar, scatter, stem | `demo_matplotlib_relation_gallery.py` |
| Matplotlib | Distribution | histogram, KDE-like density, boxplot, violin plot, ECDF | `demo_matplotlib_distribution_gallery.py` |
| Matplotlib | Categorical comparison | grouped bar, stacked bar, horizontal bar, lollipop | `demo_matplotlib_categorical_gallery.py` |
| Matplotlib | Field and vector maps | contourf, contour, pcolormesh, quiver, streamplot | `demo_matplotlib_field_gallery.py` |
| Matplotlib | 3D | surface, wireframe, projected contour | `demo_matplotlib_3d_surface.py` |
| Matplotlib | Mechanical dynamics | validation, FRF, time-frequency, phase, Poincare, bifurcation, basin | multiple nonlinear demos |
| Matplotlib | Machine learning | ROC, PR, calibration, confusion matrix, feature importance, heatmap, radar, residual KDE | multiple ML demos |
| Seaborn | Relationship | scatterplot, lineplot, regplot, residplot | `demo_seaborn_common_gallery.py` |
| Seaborn | Distribution | histplot, kdeplot, ecdfplot, rugplot | `demo_seaborn_common_gallery.py` |
| Seaborn | Categorical | barplot, boxplot, violinplot, stripplot, pointplot, countplot | `demo_seaborn_common_gallery.py` |
| Seaborn | Matrix and multivariate | heatmap, pairplot, relplot, catplot, displot | `demo_seaborn_common_gallery.py` |

## Matplotlib Common Types

Use Matplotlib templates when the paper needs precise layout control, multi-panel composition, engineering axes, custom annotations, or specialized physical plots.

| Type | Best manuscript use |
|---|---|
| line | time history, convergence, trends |
| scatter | relationship, residual structure, embedding |
| errorbar | repeated measurement with uncertainty |
| fill_between | confidence band or tolerance region |
| bar / barh | method comparison, ablation |
| stacked bar | composition across categories |
| stem | sparse term, harmonic energy, selected library term |
| histogram | empirical distribution |
| boxplot / violin | repeated-trial distribution comparison |
| contour / contourf | response surface, parameter field |
| pcolormesh / imshow | heatmap, time-frequency, matrix field |
| quiver / streamplot | vector field, flow-like dynamics |
| surface / wireframe | 3D response surface |

## Seaborn Common Types

Use Seaborn templates when the data naturally lives in a table/DataFrame and the plot needs grouping by named variables.

| Type | Best manuscript use |
|---|---|
| `scatterplot` | grouped observations and relationships |
| `lineplot` | grouped trends with confidence interval |
| `regplot` | trend line and simple regression |
| `residplot` | residual pattern check |
| `histplot` | grouped histogram |
| `kdeplot` | smooth density comparison |
| `ecdfplot` | cumulative distribution without bin choices |
| `rugplot` | raw sample locations under density |
| `barplot` | mean and uncertainty by category |
| `boxplot` | distribution summary by category |
| `violinplot` | distribution shape by category |
| `stripplot` / `swarmplot` | raw categorical samples |
| `pointplot` | category trend and uncertainty |
| `countplot` | category frequency |
| `heatmap` | correlation, confusion, coefficient matrix |
| `pairplot` | multivariate relationship screening |
| `relplot` / `catplot` / `displot` | figure-level faceted exploration |

## Practical Rule

- Use Matplotlib for final manuscript figures that need exact dimensions and annotations.
- Use Seaborn for quick statistical structure, grouped distributions, and multi-variable exploratory views.
- After exploration, convert the chosen Seaborn plot into a Matplotlib-controlled final figure if the journal layout is tight.
