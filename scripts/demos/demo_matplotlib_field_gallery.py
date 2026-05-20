# -*- coding: utf-8 -*-
"""Demo 22: contour, pseudocolor, quiver, and streamplot field maps."""

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
    apply_sci_style(base_size=8)

    x = np.linspace(-2.0, 2.0, 160)
    y = np.linspace(-2.0, 2.0, 150)
    xx, yy = np.meshgrid(x, y)
    potential = np.exp(-((xx - 0.65) ** 2 + (yy + 0.25) ** 2)) - 0.75 * np.exp(-((xx + 0.8) ** 2 + (yy - 0.55) ** 2) / 0.75)
    energy = np.sin(2.2 * xx) * np.cos(1.8 * yy) * np.exp(-0.12 * (xx**2 + yy**2))

    qx = np.linspace(-1.8, 1.8, 17)
    qy = np.linspace(-1.8, 1.8, 15)
    qxx, qyy = np.meshgrid(qx, qy)
    u = -qyy - 0.18 * qxx
    v = qxx - 0.18 * qyy

    sx = np.linspace(-2.0, 2.0, 80)
    sy = np.linspace(-2.0, 2.0, 80)
    sxx, syy = np.meshgrid(sx, sy)
    su = -syy + 0.35 * np.sin(2.0 * sxx)
    sv = sxx + 0.35 * np.cos(2.0 * syy)

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.74), constrained_layout=True)

    cf = axes[0, 0].contourf(xx, yy, potential, levels=18, cmap="coolwarm")
    axes[0, 0].contour(xx, yy, potential, levels=8, colors="black", linewidths=0.35, alpha=0.55)
    axes[0, 0].set_xlabel("$x_0$ (mm)", labelpad=2)
    axes[0, 0].set_ylabel("$v_0$ (mm/s)", labelpad=2)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0])
    cbar = fig.colorbar(cf, ax=axes[0, 0], fraction=0.046, pad=0.02)
    cbar.set_label("potential", labelpad=2)

    pc = axes[0, 1].pcolormesh(xx, yy, energy, shading="auto", cmap="viridis")
    axes[0, 1].set_xlabel("$x$ (mm)", labelpad=2)
    axes[0, 1].set_ylabel("$v$ (mm/s)", labelpad=2)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1])
    cbar = fig.colorbar(pc, ax=axes[0, 1], fraction=0.046, pad=0.02)
    cbar.set_label("energy", labelpad=2)

    axes[1, 0].quiver(qxx, qyy, u, v, color="0.20", width=0.004, scale=35)
    axes[1, 0].set_xlabel("$x$ (mm)", labelpad=2)
    axes[1, 0].set_ylabel("$v$ (mm/s)", labelpad=2)
    axes[1, 0].set_xlim(-2, 2)
    axes[1, 0].set_ylim(-2, 2)
    panel_label(axes[1, 0], "(c)")
    style_axes(axes[1, 0], grid=True)

    speed = np.hypot(su, sv)
    axes[1, 1].streamplot(sx, sy, su, sv, color=speed, cmap="plasma", linewidth=0.75, density=1.2, arrowsize=0.7)
    axes[1, 1].set_xlabel("$x$ (mm)", labelpad=2)
    axes[1, 1].set_ylabel("$v$ (mm/s)", labelpad=2)
    axes[1, 1].set_xlim(-2, 2)
    axes[1, 1].set_ylim(-2, 2)
    panel_label(axes[1, 1], "(d)")
    style_axes(axes[1, 1])

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_matplotlib_field_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
