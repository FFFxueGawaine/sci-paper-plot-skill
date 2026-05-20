# -*- coding: utf-8 -*-
"""Demo 5: SCI-style bar chart for illustrative LLM performance."""

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

    labels = ["LLM-A", "LLM-B", "LLM-C", "LLM-D", "LLM-E"]
    scores = np.array([72.4, 76.8, 81.2, 84.6, 88.1])
    colors = [
        "#9DBDD6",
        "#6EA6CC",
        SCI_PALETTE["baseline"],
        "#E07A5F",
        SCI_PALETTE["proposed"],
    ]

    fig, ax = plt.subplots(figsize=figure_size("single", 0.66), constrained_layout=True)
    x = np.arange(len(labels))
    bars = ax.bar(x, scores, width=0.62, color=colors, edgecolor="black", linewidth=0.6)

    ax.set_xlabel("LLM", labelpad=2)
    ax.set_ylabel("score (%)", labelpad=2)
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.margins(x=0.04)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)
    ax.grid(axis="x", visible=False)

    for bar, value in zip(bars, scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.3,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=7,
        )

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_bar_llm_performance", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
