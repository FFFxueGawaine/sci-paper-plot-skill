# -*- coding: utf-8 -*-
"""Demo 3: FRF / frequency-response comparison figure."""

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


def frf_curve(freq: np.ndarray, shift: float = 0.0) -> np.ndarray:
    peak_1 = 36.0 / np.sqrt((freq - (6.5 + shift)) ** 2 + 0.08)
    valley = 18.0 / np.sqrt((freq - 13.0) ** 2 + 0.20)
    peak_2 = 24.0 / np.sqrt((freq - (35.0 + shift)) ** 2 + 0.14)
    mag = -82.0 + peak_1 - valley + peak_2 - 0.18 * freq
    return mag


def main() -> None:
    apply_sci_style(base_size=10)
    freq = np.linspace(0.5, 60.0, 900)
    n4sid = frf_curve(freq, shift=0.15)
    h1_est = frf_curve(freq, shift=-0.05) + 1.4 * np.sin(freq / 2.8) * np.exp(-freq / 70)
    proposed = frf_curve(freq, shift=0.0)

    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.42), sharex=True, sharey=True, constrained_layout=True)
    for ax, offset, label in zip(axes, [0.0, -7.0], ["(a)", "(b)"]):
        ax.plot(freq, n4sid + offset, color=SCI_PALETTE["baseline"], linewidth=1.4, label="N4SID")
        ax.plot(freq, h1_est + offset, color=SCI_PALETTE["experiment"], linestyle="--", linewidth=1.2, label=r"$H_1$ estimation")
        ax.plot(freq, proposed + offset, color=SCI_PALETTE["proposed"], linestyle="-.", linewidth=1.2, label="Proposed")
        ax.set_xlabel("fre. (Hz)")
        ax.set_xlim(0, 60)
        ax.set_ylim(-130, -10)
        panel_label(ax, label)
        style_axes(ax)
        safe_legend(ax, loc="upper right", handlelength=2.0)
    axes[0].set_ylabel("mag. (dB)")

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_frf_compare", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
