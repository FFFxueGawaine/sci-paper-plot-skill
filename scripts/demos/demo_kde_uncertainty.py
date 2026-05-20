# -*- coding: utf-8 -*-
"""Demo 2: posterior scatter / uncertainty figure."""

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

from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, save_figure, style_axes


def main() -> None:
    apply_sci_style(base_size=10)
    rng = np.random.default_rng(20260519)
    mean = np.array([5600.0, 0.167])
    cov = np.array([[18.0**2, 18.0 * 0.00016 * 0.75], [18.0 * 0.00016 * 0.75, 0.00016**2]])
    samples = rng.multivariate_normal(mean, cov, size=3200)
    true_point = np.array([5610.0, 0.1673])
    estimated_point = samples.mean(axis=0)

    fig, ax = plt.subplots(figsize=figure_size("single", 0.95))
    density_color = np.hypot(samples[:, 0] - estimated_point[0], samples[:, 1] - estimated_point[1])
    density_color = 1.0 - density_color / density_color.max()
    scatter = ax.scatter(samples[:, 0], samples[:, 1], c=density_color, s=8, cmap="coolwarm", alpha=0.75, linewidths=0)
    ax.plot(true_point[0], true_point[1], "ko", markersize=4, label="true")
    ax.plot(estimated_point[0], estimated_point[1], "o", color="#9ACD32", markersize=4, label="estimated")
    ax.set_xlabel(r"$g_1(\delta_{p1})$ (N/m)")
    ax.set_ylabel(r"$\delta_{p1}$ (mm)")
    ax.text(0.05, 0.92, r"RE($\delta$): 0.41%", transform=ax.transAxes)
    ax.text(0.05, 0.84, r"RE($g$): 1.26%", transform=ax.transAxes)
    panel_label(ax, "(a)")
    style_axes(ax)
    fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_kde_uncertainty", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
