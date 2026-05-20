# -*- coding: utf-8 -*-
"""Demo 23: 3-D surface and wireframe-style response map."""

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

from scimplstyle_mssp import apply_sci_style, figure_size, save_figure


def label_3d(ax, label: str) -> None:
    ax.text2D(0.5, 1.02, label, transform=ax.transAxes, ha="center", va="bottom", fontsize=12, fontweight="bold")


def main() -> None:
    apply_sci_style(base_size=8)

    fre = np.linspace(10.0, 45.0, 80)
    amp = np.linspace(0.05, 0.45, 70)
    ff, aa = np.meshgrid(fre, amp)
    response = 0.18 + 0.95 * np.exp(-((ff - (24 + 22 * aa)) ** 2) / 32.0)
    response += 0.12 * np.sin(0.35 * ff) * np.exp(-3.0 * aa)

    fig = plt.figure(figsize=figure_size("double", 0.50), constrained_layout=True)
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")

    surf = ax1.plot_surface(ff, aa, response, cmap="viridis", linewidth=0, antialiased=True, alpha=0.96)
    ax1.set_xlabel("fre. (Hz)", labelpad=-1)
    ax1.set_ylabel("exc. amp. (N)", labelpad=-1)
    ax1.view_init(elev=26, azim=-55)
    ax1.tick_params(pad=-2)
    label_3d(ax1, "(a)")
    cbar = fig.colorbar(surf, ax=ax1, fraction=0.035, pad=0.02)
    cbar.set_label("amp. (mm)", labelpad=2)

    ax2.plot_wireframe(ff, aa, response, rstride=5, cstride=5, color="0.25", linewidth=0.55)
    ax2.contour(ff, aa, response, zdir="z", offset=response.min() - 0.10, cmap="viridis", levels=10, linewidths=0.7)
    ax2.set_zlim(response.min() - 0.10, response.max())
    ax2.set_xlabel("fre. (Hz)", labelpad=-1)
    ax2.set_ylabel("exc. amp. (N)", labelpad=-1)
    ax2.set_zlabel("resp. amp. (mm)", labelpad=-1)
    ax2.view_init(elev=26, azim=-55)
    ax2.tick_params(pad=-2)
    label_3d(ax2, "(b)")

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_matplotlib_3d_surface", out_dir=out_dir, formats=("png",), pad_inches=0.08)
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
