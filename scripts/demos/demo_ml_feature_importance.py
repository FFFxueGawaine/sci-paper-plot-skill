# -*- coding: utf-8 -*-
"""Demo 15: horizontal feature-importance chart for model interpretation."""

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

    features = ["exc. amp.", "fre.", "damping", "$k_3$", "SNR", "temp."]
    importance = np.array([0.27, 0.23, 0.18, 0.15, 0.10, 0.07])
    order = np.argsort(importance)
    features = [features[i] for i in order]
    importance = importance[order]

    fig, ax = plt.subplots(figsize=figure_size("single", 0.68), constrained_layout=True)
    colors = ["#D8E8F3"] * len(features)
    colors[-1] = SCI_PALETTE["proposed"]
    bars = ax.barh(np.arange(len(features)), importance, height=0.58, color=colors, edgecolor="black", linewidth=0.55)

    ax.set_yticks(np.arange(len(features)), features)
    ax.set_xlabel("relative importance", labelpad=2)
    ax.set_xlim(0.0, 0.31)
    ax.margins(y=0.08)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)
    ax.grid(axis="y", visible=False)

    for bar, value in zip(bars, importance):
        ax.text(value + 0.006, bar.get_y() + bar.get_height() / 2, f"{value:.2f}", va="center", fontsize=7)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_feature_importance", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
