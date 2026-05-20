# -*- coding: utf-8 -*-
"""Demo 6: phase portrait and Poincare section for nonlinear dynamics."""

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
    tau = np.linspace(0, 170 * np.pi, 9000)
    envelope = 1.0 + 0.18 * np.sin(0.045 * tau)
    x = envelope * np.sin(tau) + 0.12 * np.sin(3 * tau)
    v = envelope * np.cos(tau) + 0.08 * np.cos(3 * tau + 0.4)
    idx = np.arange(120, len(tau), 95)

    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.42), constrained_layout=True)
    axes[0].plot(x, v, color=SCI_PALETTE["experiment"], linewidth=0.55)
    axes[0].set_xlabel("dis. (mm)", labelpad=2)
    axes[0].set_ylabel("vel. (mm/s)", labelpad=2)
    panel_label(axes[0], "(a)")
    style_axes(axes[0])

    axes[1].scatter(x[idx], v[idx], s=8, color=SCI_PALETTE["proposed"], alpha=0.78, linewidths=0)
    axes[1].set_xlabel("dis. (mm)", labelpad=2)
    axes[1].set_ylabel("vel. (mm/s)", labelpad=2)
    panel_label(axes[1], "(b)")
    style_axes(axes[1], grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_phase_poincare", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
