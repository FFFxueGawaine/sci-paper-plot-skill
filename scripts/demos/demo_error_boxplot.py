# -*- coding: utf-8 -*-
"""Demo 10: method error comparison with boxplots."""

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
    labels = ["N4SID", r"$H_1$ est.", "Sparse ID", "Proposed"]
    data = [
        rng.normal(6.5, 1.2, 40),
        rng.normal(5.8, 1.0, 40),
        rng.normal(4.2, 0.8, 40),
        rng.normal(2.1, 0.55, 40),
    ]
    data = [np.clip(d, 0.2, None) for d in data]

    fig, ax = plt.subplots(figsize=figure_size("single", 0.68), constrained_layout=True)
    parts = ax.boxplot(data, patch_artist=True, widths=0.58, showfliers=False)
    colors = ["#9DBDD6", "#6EA6CC", "#E07A5F", SCI_PALETTE["proposed"]]
    for patch, color in zip(parts["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor("black")
        patch.set_linewidth(0.7)
    for key in ["whiskers", "caps", "medians"]:
        for artist in parts[key]:
            artist.set_color("black")
            artist.set_linewidth(0.7)
    ax.set_xticks(np.arange(1, len(labels) + 1), labels)
    ax.set_ylabel("relative error (%)", labelpad=2)
    ax.set_ylim(0, 9)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)
    ax.grid(axis="x", visible=False)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_error_boxplot", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
