# -*- coding: utf-8 -*-
"""Demo 18: decision boundary and 2-D embedding for dynamic states."""

from __future__ import annotations

from pathlib import Path
import sys

LOCAL_SCRIPTS = Path(__file__).resolve().parents[1]
DEFAULT_SCRIPTS = Path.home() / ".codex" / "skills" / "sci-paper-plot-skill" / "scripts"
for candidate in (LOCAL_SCRIPTS, DEFAULT_SCRIPTS):
    if (candidate / "scimplstyle_mssp.py").exists():
        sys.path.insert(0, str(candidate))
        break

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, safe_legend, save_figure, style_axes


def main() -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(51)

    centers = np.array([[-1.15, -0.55], [0.05, 0.95], [1.05, -0.35]])
    labels = ["periodic", "quasi-periodic", "chaotic"]
    colors = ["#377EB8", "#76B7B2", "#E41A1C"]
    points = []
    classes = []
    for idx, center in enumerate(centers):
        cov = np.array([[0.12, 0.025], [0.025, 0.10]]) * (1.0 + 0.18 * idx)
        pts = rng.multivariate_normal(center, cov, 70)
        points.append(pts)
        classes.append(np.full(pts.shape[0], idx))
    x = np.vstack(points)
    y = np.concatenate(classes)

    gx, gy = np.meshgrid(np.linspace(-2.0, 2.0, 240), np.linspace(-1.6, 1.8, 220))
    score = np.stack(
        [
            (gx - centers[0, 0]) ** 2 + 1.18 * (gy - centers[0, 1]) ** 2,
            0.82 * (gx - centers[1, 0]) ** 2 + (gy - centers[1, 1]) ** 2,
            1.08 * (gx - centers[2, 0]) ** 2 + 0.92 * (gy - centers[2, 1]) ** 2,
        ],
        axis=0,
    )
    region = np.argmin(score, axis=0)

    embedding = np.column_stack(
        [
            0.85 * x[:, 0] + 0.25 * np.sin(2.0 * x[:, 1]),
            0.78 * x[:, 1] + 0.22 * np.cos(1.8 * x[:, 0]),
        ]
    )

    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.43), constrained_layout=True)

    cmap = ListedColormap(["#DDEAF6", "#DDEFEA", "#F8D9D5"])
    axes[0].contourf(gx, gy, region, levels=[-0.5, 0.5, 1.5, 2.5], cmap=cmap, alpha=0.95)
    for idx, label in enumerate(labels):
        mask = y == idx
        axes[0].scatter(x[mask, 0], x[mask, 1], s=13, color=colors[idx], edgecolor="white", linewidth=0.2, label=label)
    axes[0].set_xlabel("feature 1", labelpad=2)
    axes[0].set_ylabel("feature 2", labelpad=2)
    safe_legend(axes[0], loc="upper right", handlelength=1.2)
    panel_label(axes[0], "(a)")
    style_axes(axes[0])

    for idx, label in enumerate(labels):
        mask = y == idx
        axes[1].scatter(embedding[mask, 0], embedding[mask, 1], s=15, color=colors[idx], edgecolor="white", linewidth=0.2, label=label)
    axes[1].set_xlabel("component 1", labelpad=2)
    axes[1].set_ylabel("component 2", labelpad=2)
    safe_legend(axes[1], loc="upper right", handlelength=1.2)
    panel_label(axes[1], "(b)")
    style_axes(axes[1], grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_decision_embedding", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
