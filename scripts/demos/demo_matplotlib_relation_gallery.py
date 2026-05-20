# -*- coding: utf-8 -*-
"""Demo 19: relation plots, uncertainty bands, error bars, and stem plots."""

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


def main() -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(73)

    t = np.linspace(0.0, 2.0, 220)
    mean = np.exp(-0.65 * t) * np.sin(2.0 * np.pi * 2.2 * t)
    band = 0.11 + 0.04 * np.exp(-0.8 * t)
    fre = np.array([10, 15, 20, 25, 30, 35, 40])
    amp = np.array([0.18, 0.24, 0.42, 0.70, 0.38, 0.26, 0.20])
    err = np.array([0.025, 0.030, 0.045, 0.060, 0.040, 0.032, 0.026])
    x = rng.normal(0.0, 1.0, 140)
    y = 0.62 * x + rng.normal(0.0, 0.42, x.size)
    color_value = np.hypot(x, y)
    stems = np.arange(1, 11)
    energy = np.array([0.05, 0.18, 0.42, 0.76, 0.54, 0.31, 0.20, 0.13, 0.09, 0.06])

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.72), constrained_layout=True)

    axes[0, 0].fill_between(t, mean - band, mean + band, color=SCI_PALETTE["band"], alpha=0.22, linewidth=0)
    axes[0, 0].plot(t, mean, color=SCI_PALETTE["proposed"], linewidth=1.2, label="mean")
    axes[0, 0].set_xlabel("time (s)", labelpad=2)
    axes[0, 0].set_ylabel("response (mm)", labelpad=2)
    safe_legend(axes[0, 0], loc="upper right", handlelength=1.8)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0], grid=True)

    axes[0, 1].errorbar(fre, amp, yerr=err, color=SCI_PALETTE["baseline"], marker="o", markersize=3, capsize=2.2, linewidth=1.0)
    axes[0, 1].set_xlabel("fre. (Hz)", labelpad=2)
    axes[0, 1].set_ylabel("amp. (mm)", labelpad=2)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1], grid=True)

    sc = axes[1, 0].scatter(x, y, c=color_value, s=16, cmap="viridis", edgecolor="white", linewidth=0.2)
    axes[1, 0].set_xlabel("feature 1", labelpad=2)
    axes[1, 0].set_ylabel("feature 2", labelpad=2)
    panel_label(axes[1, 0], "(c)")
    style_axes(axes[1, 0], grid=True)
    cbar = fig.colorbar(sc, ax=axes[1, 0], fraction=0.046, pad=0.02)
    cbar.set_label("radius", labelpad=2)

    markerline, stemlines, baseline = axes[1, 1].stem(stems, energy, linefmt="-", markerfmt="o", basefmt=" ")
    markerline.set_color(SCI_PALETTE["proposed"])
    markerline.set_markersize(3.5)
    stemlines.set_color(SCI_PALETTE["reference"])
    stemlines.set_linewidth(0.9)
    axes[1, 1].set_xlabel("harmonic order", labelpad=2)
    axes[1, 1].set_ylabel("energy ratio", labelpad=2)
    axes[1, 1].set_ylim(0.0, 0.85)
    panel_label(axes[1, 1], "(d)")
    style_axes(axes[1, 1], grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_matplotlib_relation_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
