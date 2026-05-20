# -*- coding: utf-8 -*-
"""Demo 20: histogram, KDE, boxplot, violin plot, and ECDF."""

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


def kde_1d(samples: np.ndarray, grid: np.ndarray, bandwidth: float) -> np.ndarray:
    scaled = (grid[:, None] - samples[None, :]) / bandwidth
    density = np.exp(-0.5 * scaled**2).sum(axis=1)
    return density / (samples.size * bandwidth * np.sqrt(2.0 * np.pi))


def main() -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(84)

    err_a = rng.normal(-0.010, 0.036, 180)
    err_b = rng.normal(0.003, 0.025, 180)
    err_c = rng.normal(0.000, 0.018, 180)
    groups = [err_a, err_b, err_c]
    names = ["N4SID", "LSTM", "Proposed"]
    grid = np.linspace(-0.13, 0.13, 240)

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.72), constrained_layout=True)

    axes[0, 0].hist(err_c, bins=20, density=True, color="#D8E8F3", edgecolor="white", linewidth=0.5)
    axes[0, 0].plot(grid, kde_1d(err_c, grid, 0.014), color=SCI_PALETTE["proposed"], linewidth=1.3)
    axes[0, 0].axvline(0.0, color=SCI_PALETTE["reference"], linewidth=0.9, linestyle="--")
    axes[0, 0].set_xlabel("error (mm)", labelpad=2)
    axes[0, 0].set_ylabel("density", labelpad=2)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0])

    box = axes[0, 1].boxplot(groups, tick_labels=names, widths=0.55, patch_artist=True, showfliers=False)
    for patch, color in zip(box["boxes"], ["#D8E8F3", "#BFD9EA", "#F6C8C4"]):
        patch.set_facecolor(color)
        patch.set_edgecolor("black")
        patch.set_linewidth(0.7)
    for key in ["whiskers", "caps", "medians"]:
        for item in box[key]:
            item.set_color("black")
            item.set_linewidth(0.7)
    axes[0, 1].set_ylabel("error (mm)", labelpad=2)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1], grid=True)
    axes[0, 1].grid(axis="x", visible=False)

    violin = axes[1, 0].violinplot(groups, showmeans=True, showmedians=False, widths=0.75)
    for body, color in zip(violin["bodies"], ["#D8E8F3", "#BFD9EA", "#F6C8C4"]):
        body.set_facecolor(color)
        body.set_edgecolor("black")
        body.set_alpha(0.9)
        body.set_linewidth(0.5)
    for key in ["cmeans", "cbars", "cmins", "cmaxes"]:
        violin[key].set_color("black")
        violin[key].set_linewidth(0.7)
    axes[1, 0].set_xticks(np.arange(1, 4), names)
    axes[1, 0].set_ylabel("error (mm)", labelpad=2)
    panel_label(axes[1, 0], "(c)")
    style_axes(axes[1, 0], grid=True)
    axes[1, 0].grid(axis="x", visible=False)

    for values, name, color in zip(groups, names, [SCI_PALETTE["reference"], SCI_PALETTE["baseline"], SCI_PALETTE["proposed"]]):
        sorted_values = np.sort(values)
        prob = np.arange(1, sorted_values.size + 1) / sorted_values.size
        axes[1, 1].plot(sorted_values, prob, color=color, linewidth=1.2, label=name)
    axes[1, 1].set_xlabel("error (mm)", labelpad=2)
    axes[1, 1].set_ylabel("cumulative prob.", labelpad=2)
    safe_legend(axes[1, 1], loc="lower right", handlelength=1.8)
    panel_label(axes[1, 1], "(d)")
    style_axes(axes[1, 1], grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_matplotlib_distribution_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
