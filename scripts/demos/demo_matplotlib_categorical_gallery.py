# -*- coding: utf-8 -*-
"""Demo 21: grouped, stacked, horizontal, and lollipop categorical charts."""

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

    cases = ["C1", "C2", "C3", "C4"]
    x = np.arange(len(cases))
    width = 0.25
    n4sid = np.array([0.092, 0.084, 0.105, 0.097])
    lstm = np.array([0.070, 0.065, 0.078, 0.071])
    proposed = np.array([0.046, 0.041, 0.052, 0.047])

    stable = np.array([74, 68, 62, 57])
    transient = np.array([18, 22, 24, 25])
    unstable = 100 - stable - transient

    labels = ["SVM", "RF", "LSTM", "PINN", "Proposed"]
    scores = np.array([0.78, 0.81, 0.86, 0.84, 0.91])
    train_time = np.array([1.2, 2.8, 8.7, 11.5, 5.6])

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.72), constrained_layout=True)

    axes[0, 0].bar(x - width, n4sid, width, color="#D8E8F3", edgecolor="black", linewidth=0.5, label="N4SID")
    axes[0, 0].bar(x, lstm, width, color=SCI_PALETTE["baseline"], edgecolor="black", linewidth=0.5, label="LSTM")
    axes[0, 0].bar(x + width, proposed, width, color=SCI_PALETTE["proposed"], edgecolor="black", linewidth=0.5, label="Proposed")
    axes[0, 0].set_xticks(x, cases)
    axes[0, 0].set_ylabel("RMSE (mm)", labelpad=2)
    axes[0, 0].set_ylim(0.0, 0.13)
    safe_legend(axes[0, 0], loc="upper left", ncol=3, handlelength=1.3, columnspacing=0.8)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0], grid=True)
    axes[0, 0].grid(axis="x", visible=False)

    axes[0, 1].bar(cases, stable, color="#D8E8F3", edgecolor="black", linewidth=0.5, label="stable")
    axes[0, 1].bar(cases, transient, bottom=stable, color="#F3D5A5", edgecolor="black", linewidth=0.5, label="transient")
    axes[0, 1].bar(cases, unstable, bottom=stable + transient, color="#F6C8C4", edgecolor="black", linewidth=0.5, label="unstable")
    axes[0, 1].set_ylabel("sample ratio (%)", labelpad=2)
    axes[0, 1].set_ylim(0, 100)
    safe_legend(axes[0, 1], outside="right", ncol=1, handlelength=1.3)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1], grid=True)
    axes[0, 1].grid(axis="x", visible=False)

    order = np.argsort(scores)
    axes[1, 0].barh(np.arange(len(labels)), scores[order], color="#D8E8F3", edgecolor="black", linewidth=0.5)
    axes[1, 0].barh(len(labels) - 1, scores[order][-1], color=SCI_PALETTE["proposed"], edgecolor="black", linewidth=0.5)
    axes[1, 0].set_yticks(np.arange(len(labels)), [labels[i] for i in order])
    axes[1, 0].set_xlabel("classification score", labelpad=2)
    axes[1, 0].set_xlim(0.72, 0.94)
    panel_label(axes[1, 0], "(c)")
    style_axes(axes[1, 0], grid=True)
    axes[1, 0].grid(axis="y", visible=False)

    axes[1, 1].hlines(labels, 0, train_time, color="0.35", linewidth=0.9)
    axes[1, 1].plot(train_time, labels, "o", color=SCI_PALETTE["baseline"], markersize=3.5)
    axes[1, 1].set_xlabel("training time (s)", labelpad=2)
    panel_label(axes[1, 1], "(d)")
    style_axes(axes[1, 1], grid=True)
    axes[1, 1].grid(axis="y", visible=False)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_matplotlib_categorical_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
