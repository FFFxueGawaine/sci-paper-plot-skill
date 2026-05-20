# -*- coding: utf-8 -*-
"""Demo 13: predicted-versus-true regression plot with residual panel."""

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
    rng = np.random.default_rng(24)

    true_amp = np.linspace(0.15, 1.15, 95)
    noise = rng.normal(0.0, 0.035, true_amp.size)
    pred_amp = 0.02 + 0.965 * true_amp + noise
    residual = pred_amp - true_amp
    r2 = 1.0 - np.sum(residual**2) / np.sum((true_amp - true_amp.mean()) ** 2)

    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.42), constrained_layout=True)

    axes[0].scatter(true_amp, pred_amp, s=16, color=SCI_PALETTE["baseline"], alpha=0.78, edgecolor="white", linewidth=0.25)
    axes[0].plot([0.1, 1.2], [0.1, 1.2], color=SCI_PALETTE["reference"], linewidth=1.0, linestyle="--", label="ideal")
    axes[0].set_xlim(0.1, 1.2)
    axes[0].set_ylim(0.1, 1.2)
    axes[0].set_xlabel("true peak amp. (mm)", labelpad=2)
    axes[0].set_ylabel("predicted peak amp. (mm)", labelpad=2)
    axes[0].text(0.16, 1.08, rf"$R^2={r2:.3f}$", fontsize=8)
    safe_legend(axes[0], loc="lower right", handlelength=1.8)
    panel_label(axes[0], "(a)")
    style_axes(axes[0], grid=True)

    axes[1].scatter(true_amp, residual, s=16, color=SCI_PALETTE["proposed"], alpha=0.75, edgecolor="white", linewidth=0.25)
    axes[1].axhline(0.0, color=SCI_PALETTE["reference"], linewidth=1.0, linestyle="--")
    axes[1].set_xlim(0.1, 1.2)
    axes[1].set_ylim(-0.12, 0.12)
    axes[1].set_xlabel("true peak amp. (mm)", labelpad=2)
    axes[1].set_ylabel("residual (mm)", labelpad=2)
    panel_label(axes[1], "(b)")
    style_axes(axes[1], grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_ml_prediction_truth", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
