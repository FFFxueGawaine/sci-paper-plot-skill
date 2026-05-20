# -*- coding: utf-8 -*-
"""Demo 9: basin-of-attraction style classification map."""

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

from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, save_figure, style_axes


def main() -> None:
    apply_sci_style(base_size=8)
    x0 = np.linspace(-1.2, 1.2, 180)
    v0 = np.linspace(-1.0, 1.0, 160)
    xx, vv = np.meshgrid(x0, v0)
    score = xx**2 + 0.8 * vv**2 + 0.45 * np.sin(4.0 * xx) - 0.25 * np.cos(5.0 * vv)
    basin = np.where(score < 0.42, 0, np.where(xx + 0.25 * vv > 0.18, 1, 2))

    cmap = ListedColormap(["#8FBBD9", "#E76F51", "#4D4D4D"])
    fig, ax = plt.subplots(figsize=figure_size("single", 0.78), constrained_layout=True)
    mesh = ax.pcolormesh(x0, v0, basin, shading="nearest", cmap=cmap, vmin=0, vmax=2)
    ax.contour(x0, v0, score, levels=[0.42], colors="black", linewidths=0.7)
    ax.set_xlabel(r"$x_0$ (mm)", labelpad=2)
    ax.set_ylabel(r"$v_0$ (mm/s)", labelpad=2)
    panel_label(ax, "(a)")
    style_axes(ax)
    cbar = fig.colorbar(mesh, ax=ax, ticks=[0.33, 1.0, 1.67], fraction=0.045, pad=0.025)
    cbar.ax.set_yticklabels(["A1", "A2", "A3"])

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_basin_attraction", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
