# -*- coding: utf-8 -*-
"""Demo 4: SCI-style line plot with multiple curves."""

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

    t = np.linspace(0.0, 10.0, 41)
    proposed = 0.82 + 0.15 * (1.0 - np.exp(-0.35 * t))
    baseline = 0.78 + 0.12 * (1.0 - np.exp(-0.22 * t))
    reference = 0.80 + 0.10 * np.log1p(t) / np.log(11.0)

    fig, ax = plt.subplots(figsize=figure_size("single", 0.66), constrained_layout=True)
    ax.plot(t, proposed, color=SCI_PALETTE["proposed"], marker="o", markersize=2.6, linewidth=1.1, label="Proposed")
    ax.plot(t, baseline, color=SCI_PALETTE["baseline"], marker="s", markersize=2.4, linewidth=1.0, label="Baseline")
    ax.plot(t, reference, color=SCI_PALETTE["reference"], marker="^", markersize=2.4, linewidth=1.0, label="Reference")

    ax.set_xlabel("time (s)", labelpad=2)
    ax.set_ylabel(r"$R^2$", labelpad=2)
    ax.set_xlim(0, 10)
    ax.set_ylim(0.76, 1.01)
    ax.margins(x=0.01, y=0.03)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)
    safe_legend(ax, 
        loc="lower right",
        fontsize=7,
        handlelength=1.5,
        handletextpad=0.5,
        borderpad=0.3,
        labelspacing=0.25,
        borderaxespad=0.4,
    )

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_line_plot", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
