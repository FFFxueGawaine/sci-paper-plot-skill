# -*- coding: utf-8 -*-
"""Demo 17: common ML classification and training curves."""

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


def auc_trapz(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.trapz(y, x))


def main() -> None:
    apply_sci_style(base_size=8)

    fpr = np.linspace(0.0, 1.0, 160)
    roc_curves = {
        "SVM": 1.0 - (1.0 - fpr) ** 2.4,
        "LSTM": 1.0 - (1.0 - fpr) ** 3.0,
        "Proposed": 1.0 - (1.0 - fpr) ** 4.6,
    }
    recall = np.linspace(0.0, 1.0, 160)
    pr_curves = {
        "SVM": 0.90 - 0.33 * recall**1.55,
        "LSTM": 0.94 - 0.27 * recall**1.65,
        "Proposed": 0.98 - 0.18 * recall**1.85,
    }
    colors = {"SVM": SCI_PALETTE["reference"], "LSTM": SCI_PALETTE["baseline"], "Proposed": SCI_PALETTE["proposed"]}

    prob = np.linspace(0.08, 0.92, 9)
    obs = np.clip(prob + np.array([-0.05, -0.03, -0.01, 0.02, 0.01, 0.02, -0.01, 0.00, 0.03]), 0, 1)
    n_train = np.array([30, 60, 120, 240, 480, 960])
    train_score = np.array([0.96, 0.94, 0.925, 0.915, 0.905, 0.900])
    val_score = np.array([0.70, 0.78, 0.84, 0.875, 0.890, 0.898])

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.72), constrained_layout=True)

    for name, tpr in roc_curves.items():
        axes[0, 0].plot(fpr, tpr, color=colors[name], linewidth=1.2, label=f"{name}, AUC={auc_trapz(fpr, tpr):.2f}")
    axes[0, 0].plot([0, 1], [0, 1], color="0.45", linewidth=0.9, linestyle="--")
    axes[0, 0].set_xlabel("false positive rate", labelpad=2)
    axes[0, 0].set_ylabel("true positive rate", labelpad=2)
    safe_legend(axes[0, 0], loc="lower right", handlelength=1.8)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0], grid=True)

    for name, precision in pr_curves.items():
        axes[0, 1].plot(recall, precision, color=colors[name], linewidth=1.2, label=name)
    axes[0, 1].set_xlabel("recall", labelpad=2)
    axes[0, 1].set_ylabel("precision", labelpad=2)
    axes[0, 1].set_ylim(0.55, 1.02)
    safe_legend(axes[0, 1], loc="lower left", handlelength=1.8)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1], grid=True)

    axes[1, 0].plot([0, 1], [0, 1], color="0.45", linewidth=0.9, linestyle="--", label="ideal")
    axes[1, 0].plot(prob, obs, color=SCI_PALETTE["proposed"], marker="o", markersize=3, linewidth=1.1, label="model")
    axes[1, 0].set_xlabel("predicted probability", labelpad=2)
    axes[1, 0].set_ylabel("observed frequency", labelpad=2)
    safe_legend(axes[1, 0], loc="upper left", handlelength=1.8)
    panel_label(axes[1, 0], "(c)")
    style_axes(axes[1, 0], grid=True)

    axes[1, 1].plot(n_train, train_score, color=SCI_PALETTE["baseline"], marker="s", markersize=3, label="train")
    axes[1, 1].plot(n_train, val_score, color=SCI_PALETTE["proposed"], marker="o", markersize=3, label="validation")
    axes[1, 1].set_xscale("log")
    axes[1, 1].set_xlabel("training samples", labelpad=2)
    axes[1, 1].set_ylabel("score", labelpad=2)
    axes[1, 1].set_ylim(0.65, 1.00)
    safe_legend(axes[1, 1], loc="lower right", handlelength=1.8)
    panel_label(axes[1, 1], "(d)")
    style_axes(axes[1, 1], grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_classification_curves", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
