# Matplotlib Gallery Examples for SCI-Style Papers

This gallery organizes common Matplotlib plots by manuscript purpose. It is not intended to cover every Matplotlib API call; it covers the plot families most often useful in engineering and machine-learning manuscripts.

## Added Gallery Demos

| Figure family | Main plot types covered | Template file |
|---|---|---|
| ML classification curves | ROC, PR, calibration, learning curve | `demo_ml_classification_curves.py` |
| ML state visualization | decision boundary, 2-D embedding | `demo_ml_decision_embedding.py` |
| Relation and uncertainty | confidence band, errorbar, color scatter, stem plot | `demo_matplotlib_relation_gallery.py` |
| Distributions | histogram, KDE, boxplot, violin plot, ECDF | `demo_matplotlib_distribution_gallery.py` |
| Categorical comparisons | grouped bar, stacked bar, horizontal bar, lollipop chart | `demo_matplotlib_categorical_gallery.py` |
| Field maps | contourf, contour, pcolormesh, quiver, streamplot | `demo_matplotlib_field_gallery.py` |
| 3-D maps | surface, wireframe, projected contour | `demo_matplotlib_3d_surface.py` |
| Seaborn common gallery | scatterplot, lineplot, regplot, residplot, histplot, kdeplot, ecdfplot, rugplot, boxplot, violinplot, stripplot, swarmplot, barplot, pointplot, countplot, heatmap, pairplot, relplot, catplot, displot | `demo_seaborn_common_gallery.py` |

## Guidance for New Users

- Start from the figure family that matches the manuscript question.
- Use line plots, error bars, and boxplots for precise comparisons.
- Use radar charts, 3-D surfaces, and complex field maps sparingly because they are visually heavier.
- Use heatmaps and contour maps when the x-y grid has physical meaning.
- Use decision boundaries and embeddings only when they explain model behavior better than a table.
- Use Seaborn when the data is already a tidy `DataFrame` and the paper figure needs grouped statistics or quick faceting; see `references/common-plot-types-catalog.md`.
- Avoid pie charts in SCI manuscripts unless the composition is the central result.
