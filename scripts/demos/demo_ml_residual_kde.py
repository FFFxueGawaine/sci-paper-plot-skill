# -*- coding: utf-8 -*-
"""Demo 14: residual trend and error-density plot."""

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

from scimplstyle_mssp import SCI_PALETTE, apply_sci_style, figure_size, panel_label, safe_legend, save_figure, style_axes


def gaussian_kde_1d(samples: np.ndarray, grid: np.ndarray, bandwidth: float) -> np.ndarray:
    scaled = (grid[:, None] - samples[None, :]) / bandwidth
    density = np.exp(-0.5 * scaled**2).sum(axis=1)
    return density / (samples.size * bandwidth * np.sqrt(2 * np.pi))


def main() -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(32)

    fre = np.linspace(5.0, 55.0, 160)
    residual = 0.012 * np.sin(0.45 * fre) + rng.normal(0.0, 0.025, fre.size)
    residual += 0.0006 * (fre - 30.0)
    grid = np.linspace(-0.12, 0.12, 240)
    density = gaussian_kde_1d(residual, grid, bandwidth=0.018)

    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.42), constrained_layout=True)

    axes[0].scatter(fre, residual, s=13, color=SCI_PALETTE["baseline"], alpha=0.74, edgecolor="white", linewidth=0.2)
    axes[0].axhline(0.0, color=SCI_PALETTE["reference"], linewidth=1.0, linestyle="--")
    axes[0].set_xlabel("fre. (Hz)", labelpad=2)
    axes[0].set_ylabel("residual (mm)", labelpad=2)
    axes[0].set_ylim(-0.12, 0.12)
    panel_label(axes[0], "(a)")
    style_axes(axes[0], grid=True)

    axes[1].hist(residual, bins=18, density=True, color="#D8E8F3", edgecolor="white", linewidth=0.5)
    axes[1].plot(grid, density, color=SCI_PALETTE["proposed"], linewidth=1.4, label="KDE")
    axes[1].axvline(0.0, color=SCI_PALETTE["reference"], linewidth=1.0, linestyle="--")
    axes[1].set_xlabel("residual (mm)", labelpad=2)
    axes[1].set_ylabel("density", labelpad=2)
    safe_legend(axes[1], loc="upper left", handlelength=1.8)
    panel_label(axes[1], "(b)")
    style_axes(axes[1])

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_residual_kde", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
