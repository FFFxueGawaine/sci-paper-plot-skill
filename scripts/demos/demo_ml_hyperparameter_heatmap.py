# -*- coding: utf-8 -*-
"""Demo 16: hyperparameter heatmap for validation error."""

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

from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, save_figure


def main() -> None:
    apply_sci_style(base_size=8)

    hidden_units = np.array([16, 32, 64, 128, 256])
    learning_rates = np.array([1e-4, 3e-4, 1e-3, 3e-3, 1e-2])
    x = np.linspace(-1.0, 1.0, hidden_units.size)
    y = np.linspace(-1.0, 1.0, learning_rates.size)
    xx, yy = np.meshgrid(x, y)
    rmse = 0.035 + 0.020 * xx**2 + 0.028 * (yy + 0.15) ** 2
    rmse += np.array(
        [
            [0.016, 0.010, 0.006, 0.008, 0.014],
            [0.011, 0.006, 0.002, 0.005, 0.011],
            [0.008, 0.003, 0.000, 0.004, 0.010],
            [0.014, 0.007, 0.006, 0.010, 0.020],
            [0.026, 0.019, 0.017, 0.024, 0.038],
        ]
    )

    fig, ax = plt.subplots(figsize=figure_size("single", 0.84), constrained_layout=True)
    im = ax.imshow(rmse, cmap="viridis_r", origin="lower")

    ax.set_xlabel("hidden units", labelpad=2)
    ax.set_ylabel("learning rate", labelpad=2)
    ax.set_xticks(np.arange(hidden_units.size), [str(v) for v in hidden_units])
    ax.set_yticks(np.arange(learning_rates.size), [r"$10^{-4}$", r"$3\times10^{-4}$", r"$10^{-3}$", r"$3\times10^{-3}$", r"$10^{-2}$"])
    ax.tick_params(length=0)
    panel_label(ax, "(a)")

    best = np.unravel_index(np.argmin(rmse), rmse.shape)
    ax.scatter(best[1], best[0], marker="*", s=85, color="white", edgecolor="black", linewidth=0.55)
    ax.text(best[1] + 0.18, best[0] + 0.18, "best", color="black", fontsize=7, weight="bold")

    for edge in ax.spines.values():
        edge.set_visible(False)
    ax.set_xticks(np.arange(-0.5, hidden_units.size, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, learning_rates.size, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.7)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("RMSE (mm)", labelpad=2)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_hyperparameter_heatmap", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
