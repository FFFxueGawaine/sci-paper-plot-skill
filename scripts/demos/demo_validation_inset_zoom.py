# -*- coding: utf-8 -*-
"""Demo 27: validation curve with a local zoom inset."""

from __future__ import annotations

from pathlib import Path
import sys

LOCAL_SCRIPTS = Path(__file__).resolve().parents[1]
DEFAULT_SCRIPTS = Path.home() / ".codex" / "skills" / "sci-paper-plot-skill" / "scripts"
for candidate in (LOCAL_SCRIPTS, DEFAULT_SCRIPTS):
    if (candidate / "scimplstyle_mssp.py").exists():
        sys.path.insert(0, str(candidate))
        break

import matplotlib.pyplot as plt
import numpy as np

from scimplstyle_mssp import SCI_PALETTE, add_zoom_inset, apply_sci_style, figure_size, panel_label, safe_legend, save_figure, style_axes


def main() -> None:
    apply_sci_style(base_size=8)

    time = np.linspace(0.0, 5.0, 1500)
    ramp = 1.0 / (1.0 + np.exp(-5.0 * (time - 1.05)))
    envelope = ramp * np.exp(-0.08 * np.maximum(time - 1.05, 0.0))
    exp = envelope * (np.sin(2 * np.pi * 1.18 * time) + 0.14 * np.sin(2 * np.pi * 4.2 * time))
    pred = exp + 0.024 * envelope * np.sin(2 * np.pi * 0.72 * time + 0.5)

    fig, ax = plt.subplots(figsize=figure_size("single", 0.68), constrained_layout=True)
    ax.plot(time, exp, color=SCI_PALETTE["experiment"], lw=1.1, label="exp.")
    ax.plot(time, pred, color=SCI_PALETTE["identified"], lw=1.1, ls="--", label="id.")
    ax.set_xlabel("time (s)", labelpad=2)
    ax.set_ylabel("acc. (m/s$^2$)", labelpad=2)
    ax.set_xlim(0.0, 5.0)
    ax.set_ylim(-1.18, 1.85)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)
    safe_legend(ax, loc="upper right", ncol=2)

    xlim = (2.45, 2.92)
    mask = (time >= xlim[0]) & (time <= xlim[1])
    ymin = min(exp[mask].min(), pred[mask].min()) - 0.035
    ymax = max(exp[mask].max(), pred[mask].max()) + 0.035
    inset = add_zoom_inset(
        ax,
        xlim=xlim,
        ylim=(ymin, ymax),
        loc="upper left",
        width="31%",
        height="24%",
        connectors=(1, 3),
        ypad_fraction=0.12,
    )
    inset.plot(time, exp, color=SCI_PALETTE["experiment"], lw=0.9)
    inset.plot(time, pred, color=SCI_PALETTE["identified"], lw=0.9, ls="--")
    inset.set_xlabel("")
    inset.set_ylabel("")

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_validation_inset_zoom", out_dir=out_dir, formats=("png",), pad_inches=0.08)
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
