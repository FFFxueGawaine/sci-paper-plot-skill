# -*- coding: utf-8 -*-
"""Demo 26: sparse nonlinear library and validation residual plots."""

from __future__ import annotations

from pathlib import Path
import sys

LOCAL_SCRIPTS = Path(__file__).resolve().parents[1]
DEFAULT_SCRIPTS = Path.home() / ".codex" / "skills" / "sci-paper-plot-skill" / "scripts"
for candidate in (LOCAL_SCRIPTS, DEFAULT_SCRIPTS):
    if (candidate / "scimplstyle_mssp.py").exists():
        sys.path.insert(0, str(candidate))
        break

import matplotlib.pyplot as plt
import numpy as np

from scimplstyle_mssp import SCI_PALETTE, apply_sci_style, figure_size, panel_label, safe_legend, save_figure, style_axes


def main() -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(20260520)

    terms = [r"$x$", r"$\dot{x}$", r"$x^2$", r"$x\dot{x}$", r"$x^3$", r"$\sin x$", r"$\cos \Omega t$"]
    true_coef = np.array([-1.00, -0.08, 0.00, 0.00, -0.90, 0.00, 0.28])
    id_coef = np.array([-1.02, -0.074, 0.012, -0.015, -0.87, 0.006, 0.276])

    time = np.linspace(0.0, 8.0, 900)
    residual = 0.012 * np.exp(-0.24 * time) * np.sin(2 * np.pi * 2.3 * time) + 0.0035 * rng.standard_normal(time.size)

    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.44), constrained_layout=True)

    ax = axes[0]
    y = np.arange(len(terms))
    height = 0.34
    ax.barh(y - height / 2, true_coef, height=height, color="#D8E8F3", edgecolor="black", linewidth=0.55, label="true")
    ax.barh(y + height / 2, id_coef, height=height, color=SCI_PALETTE["proposed"], edgecolor="black", linewidth=0.55, label="id.")
    ax.axvline(0.0, color="0.25", lw=0.65)
    ax.set_yticks(y, terms)
    ax.set_xlabel("coef. value", labelpad=2)
    ax.set_xlim(-1.16, 0.42)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)
    ax.grid(axis="y", visible=False)
    safe_legend(ax, loc="upper left", ncol=2)

    ax = axes[1]
    ax.plot(time, residual, color=SCI_PALETTE["identified"], lw=0.85)
    ax.axhline(0.0, color="0.25", lw=0.60)
    ax.set_xlabel("time (s)", labelpad=2)
    ax.set_ylabel("pred. err. (mm)", labelpad=2)
    ax.set_xlim(time.min(), time.max())
    panel_label(ax, "(b)")
    style_axes(ax, grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_nonlinear_identification_library", out_dir=out_dir, formats=("png",), pad_inches=0.05)
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
