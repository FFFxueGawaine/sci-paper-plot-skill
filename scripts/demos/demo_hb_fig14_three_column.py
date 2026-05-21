# -*- coding: utf-8 -*-
"""Fig. 14-style one-row three-column time-response demo."""

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

from scimplstyle_mssp import SCI_PALETTE, apply_sci_style, figure_size, panel_label, save_figure, style_axes


def synthetic_clearance_response(
    time: np.ndarray,
    carrier_hz: float,
    beat_hz: float,
    impact_time: float,
    amplitude: float,
) -> np.ndarray:
    envelope = 0.42 + 0.34 * np.sin(2.0 * np.pi * beat_hz * time) ** 2
    base = amplitude * envelope * np.sin(2.0 * np.pi * carrier_hz * time)
    impact = 0.10 * amplitude * np.exp(-((time - impact_time) / 0.75) ** 2)
    impact *= np.sin(2.0 * np.pi * (carrier_hz * 2.7) * time)
    return base + impact


def main() -> None:
    apply_sci_style(base_size=7)

    time = np.linspace(0.0, 60.0, 1800)
    series = [
        synthetic_clearance_response(time, carrier_hz=0.42, beat_hz=0.022, impact_time=18.0, amplitude=0.18),
        synthetic_clearance_response(time, carrier_hz=0.55, beat_hz=0.018, impact_time=31.0, amplitude=0.26),
        synthetic_clearance_response(time, carrier_hz=0.68, beat_hz=0.015, impact_time=43.0, amplitude=0.34),
    ]
    labels = [r"$x_1$", r"$x_2$", r"$x_3$"]

    fig, axes = plt.subplots(1, 3, figsize=figure_size("double", 0.24), sharex=True, constrained_layout=True)
    for index, (ax, response, ylabel) in enumerate(zip(axes, series, labels)):
        ax.plot(time, response, color=SCI_PALETTE["experiment"], linewidth=0.85)
        ax.axhline(0.0, color="0.70", linewidth=0.5, zorder=0)
        ax.set_xlim(0.0, 60.0)
        ax.set_xlabel("time (s)", labelpad=1)
        ax.set_ylabel(f"{ylabel} (mm)", labelpad=1)
        ax.set_ylim(-0.48, 0.48)
        panel_label(ax, f"({chr(97 + index)})", size=9)
        style_axes(ax)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_hb_fig14_three_column", out_dir=out_dir, formats=("png",))
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
