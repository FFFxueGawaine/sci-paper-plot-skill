# -*- coding: utf-8 -*-
"""Demo 12: compact confusion matrix for dynamic-state classification."""

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

from scimplstyle_mssp import apply_sci_style, figure_size, panel_label, save_figure


def main() -> None:
    apply_sci_style(base_size=8)

    labels = ["P", "QP", "C", "Jump"]
    counts = np.array(
        [
            [54, 3, 1, 2],
            [4, 49, 5, 2],
            [1, 4, 52, 3],
            [2, 2, 4, 52],
        ],
        dtype=float,
    )
    cm = counts / counts.sum(axis=1, keepdims=True) * 100.0

    fig, ax = plt.subplots(figsize=figure_size("single", 0.83), constrained_layout=True)
    im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=100)

    ax.set_xlabel("predicted class", labelpad=2)
    ax.set_ylabel("true class", labelpad=2)
    ax.set_xticks(np.arange(len(labels)), labels)
    ax.set_yticks(np.arange(len(labels)), labels)
    ax.tick_params(length=0)
    panel_label(ax, "(a)")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            text_color = "white" if cm[i, j] > 55 else "black"
            ax.text(j, i, f"{cm[i, j]:.0f}", ha="center", va="center", fontsize=7, color=text_color)

    for edge in ax.spines.values():
        edge.set_visible(False)
    ax.set_xticks(np.arange(-0.5, len(labels), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(labels), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.8)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cbar.set_label("accuracy (%)", labelpad=2)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_confusion_matrix", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
