# -*- coding: utf-8 -*-
"""Demo 11: radar chart for normalized ML model performance."""

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

from scimplstyle_mssp import SCI_PALETTE, apply_sci_style, figure_size, panel_label, safe_legend, save_figure


def main() -> None:
    apply_sci_style(base_size=8)

    metrics = ["Accuracy", "Robust.", "Speed", "Data eff.", "Stability"]
    theta = np.linspace(0.0, 2 * np.pi, len(metrics), endpoint=False)
    theta = np.r_[theta, theta[0]]

    model_scores = {
        "SVM": [0.70, 0.58, 0.88, 0.72, 0.66],
        "LSTM": [0.82, 0.75, 0.48, 0.61, 0.73],
        "PINN": [0.78, 0.86, 0.55, 0.78, 0.82],
        "Proposed": [0.91, 0.88, 0.74, 0.84, 0.90],
    }
    colors = {
        "SVM": SCI_PALETTE["reference"],
        "LSTM": SCI_PALETTE["baseline"],
        "PINN": SCI_PALETTE["band"],
        "Proposed": SCI_PALETTE["proposed"],
    }

    fig, ax = plt.subplots(
        figsize=figure_size("single", 0.95),
        subplot_kw={"projection": "polar"},
        constrained_layout=True,
    )

    for name, values in model_scores.items():
        closed = np.r_[values, values[0]]
        ax.plot(theta, closed, marker="o", markersize=3, linewidth=1.1, color=colors[name], label=name)
        ax.fill(theta, closed, color=colors[name], alpha=0.08)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(theta[:-1], metrics)
    ax.set_ylim(0.0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=7)
    ax.tick_params(pad=2)
    ax.grid(color="0.82", linewidth=0.5)
    ax.spines["polar"].set_linewidth(0.8)
    panel_label(ax, "(a)", y=1.08)
    safe_legend(ax, loc="lower center", bbox_to_anchor=(0.5, -0.23), ncol=2, frameon=True, handlelength=1.6)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_radar_chart", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
