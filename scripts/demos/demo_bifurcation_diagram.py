# -*- coding: utf-8 -*-
"""Demo 7: bifurcation-style diagram with synthetic response peaks."""

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
    rng = np.random.default_rng(20260519)
    omega = np.linspace(0.72, 1.28, 150)
    xs = []
    ys = []
    for w in omega:
        base = 0.18 + 0.55 / (1 + 70 * (w - 1.02) ** 2)
        branches = [base]
        if 0.91 < w < 1.17:
            branches.append(base - 0.16 - 0.04 * np.cos(24 * w))
        if 1.04 < w < 1.22:
            branches.append(base + 0.12 + 0.03 * np.sin(35 * w))
        for b in branches:
            y = b + 0.006 * rng.standard_normal(12)
            xs.extend([w] * len(y))
            ys.extend(y)

    fig, ax = plt.subplots(figsize=figure_size("single", 0.68), constrained_layout=True)
    ax.scatter(xs, ys, s=2.8, color=SCI_PALETTE["experiment"], alpha=0.62, linewidths=0)
    ax.axvspan(0.91, 1.17, color=SCI_PALETTE["band"], alpha=0.16, linewidth=0)
    ax.set_xlabel(r"excitation frequency ratio $\Omega$", labelpad=2)
    ax.set_ylabel("peak dis. (mm)", labelpad=2)
    ax.set_xlim(0.72, 1.28)
    ax.set_ylim(0.0, 1.1)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_bifurcation_diagram", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
