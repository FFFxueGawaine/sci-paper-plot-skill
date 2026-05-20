# -*- coding: utf-8 -*-
"""Demo 1: model validation / prediction comparison figure."""

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
    apply_sci_style(base_size=10)
    t = np.linspace(0.0, 6.0, 1200)
    experiment = np.sin(2 * np.pi * 1.6 * t) * np.exp(-0.08 * t)
    experiment += 0.35 * np.sin(2 * np.pi * 4.2 * t) * np.exp(-0.16 * t)
    identified = experiment + 0.035 * np.sin(2 * np.pi * 0.55 * t + 0.3)

    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.42), sharex=True, constrained_layout=True)
    for ax, scale, label in zip(axes, [1.0, 0.65], ["(a)", "(b)"]):
        ax.plot(t, scale * experiment, color=SCI_PALETTE["experiment"], linewidth=1.2, label="experiment")
        ax.plot(t, scale * identified, color=SCI_PALETTE["identified"], linestyle="--", linewidth=1.2, label="identified")
        ax.set_xlabel("time (s)")
        ax.set_xlim(0, 6)
        style_axes(ax)
        panel_label(ax, label)
        safe_legend(ax, loc="upper right", handlelength=2.0)
    axes[0].set_ylabel(r"$y$ (m/s$^2$)")

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_validation_compare", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
