# -*- coding: utf-8 -*-
"""Demo 8: time response plus time-frequency map."""

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

from scimplstyle_mssp import SCI_PALETTE, apply_sci_style, figure_size, panel_label, save_figure, style_axes


def main() -> None:
    apply_sci_style(base_size=8)
    t = np.linspace(0.0, 60.0, 1400)
    response = 0.22 * np.sin(2 * np.pi * (5 + 0.18 * t) * t / 8)
    response += 0.08 * np.sin(2 * np.pi * 12.0 * t) * np.exp(-0.025 * t)

    tt = np.linspace(0.0, 60.0, 240)
    ff = np.linspace(0.0, 60.0, 180)
    ridge1 = 6 + 0.78 * tt
    ridge2 = 10 + 0.12 * tt
    amp = np.exp(-((ff[:, None] - ridge1[None, :]) ** 2) / 14)
    amp += 0.55 * np.exp(-((ff[:, None] - ridge2[None, :]) ** 2) / 8)
    amp += 0.08 * np.sin(0.4 * tt)[None, :] ** 2

    fig, axes = plt.subplots(2, 1, figsize=figure_size("double", 0.56), sharex=True, constrained_layout=True)
    axes[0].plot(t, response, color=SCI_PALETTE["experiment"], linewidth=0.8)
    axes[0].set_ylabel("dis. (mm)", labelpad=2)
    panel_label(axes[0], "(a)")
    style_axes(axes[0])

    mesh = axes[1].pcolormesh(tt, ff, amp, shading="auto", cmap="viridis")
    axes[1].set_xlabel("time (s)", labelpad=2)
    axes[1].set_ylabel("fre. (Hz)", labelpad=2)
    axes[1].set_ylim(0, 60)
    panel_label(axes[1], "(b)")
    style_axes(axes[1])
    cbar = fig.colorbar(mesh, ax=axes[1], fraction=0.025, pad=0.015)
    cbar.set_label("energy", labelpad=2)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_time_frequency_map", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
