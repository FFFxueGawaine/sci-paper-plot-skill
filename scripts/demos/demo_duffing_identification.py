# -*- coding: utf-8 -*-
"""Demo 24: Duffing oscillator analysis and identification plots."""

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

from scimplstyle_mssp import SCI_PALETTE, apply_sci_style, figure_size, panel_label, safe_legend, save_figure, style_axes


def duffing_rhs(state: np.ndarray, time: float, params: tuple[float, float, float, float, float]) -> np.ndarray:
    c, k, alpha, force, omega = params
    dis, vel = state
    acc = force * np.cos(omega * time) - c * vel - k * dis - alpha * dis**3
    return np.array([vel, acc])


def rk4_step(state: np.ndarray, time: float, dt: float, params: tuple[float, float, float, float, float]) -> np.ndarray:
    k1 = duffing_rhs(state, time, params)
    k2 = duffing_rhs(state + 0.5 * dt * k1, time + 0.5 * dt, params)
    k3 = duffing_rhs(state + 0.5 * dt * k2, time + 0.5 * dt, params)
    k4 = duffing_rhs(state + dt * k3, time + dt, params)
    return state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def simulate_duffing(params: tuple[float, float, float, float, float], dt: float = 0.005, end: float = 24.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    time = np.arange(0.0, end + dt, dt)
    states = np.zeros((time.size, 2))
    states[0] = np.array([0.18, 0.0])
    for i in range(1, time.size):
        states[i] = rk4_step(states[i - 1], time[i - 1], dt, params)
    return time, states[:, 0], states[:, 1]


def main() -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(20260520)

    true_params = np.array([0.080, 1.000, 0.900, 0.280, 1.050])
    time, dis_true, vel_true = simulate_duffing(tuple(true_params))
    dis_meas = dis_true + 0.0015 * rng.standard_normal(dis_true.size)
    identified = true_params[:4] * np.array([0.94, 1.025, 0.96, 1.035])
    identified_params = np.r_[identified[:4], true_params[-1]]
    _, dis_id, vel_id = simulate_duffing(tuple(identified_params))

    window = time > 17.5
    x_grid = np.linspace(dis_meas[window].min() * 1.12, dis_meas[window].max() * 1.12, 300)
    force_true = true_params[1] * x_grid + true_params[2] * x_grid**3
    force_id = identified[1] * x_grid + identified[2] * x_grid**3

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.62), constrained_layout=True)

    ax = axes[0, 0]
    ax.plot(time[window], dis_meas[window], color=SCI_PALETTE["experiment"], lw=0.9, label="meas.")
    ax.plot(time[window], dis_id[window], color=SCI_PALETTE["identified"], lw=1.0, ls="--", label="id.")
    ax.set_xlabel("time (s)", labelpad=2)
    ax.set_ylabel("dis. (mm)", labelpad=2)
    panel_label(ax, "(a)")
    style_axes(ax, grid=True)
    safe_legend(ax, loc="upper right", ncol=2)

    ax = axes[0, 1]
    ax.plot(dis_meas[window], vel_true[window], color=SCI_PALETTE["experiment"], lw=0.55)
    ax.plot(dis_id[window], vel_id[window], color=SCI_PALETTE["identified"], lw=0.75, ls="--")
    ax.set_xlabel("dis. (mm)", labelpad=2)
    ax.set_ylabel("vel. (mm/s)", labelpad=2)
    panel_label(ax, "(b)")
    style_axes(ax, grid=True)

    ax = axes[1, 0]
    ax.plot(x_grid, force_true, color=SCI_PALETTE["experiment"], lw=1.1, label="true")
    ax.plot(x_grid, force_id, color=SCI_PALETTE["identified"], lw=1.1, ls="--", label="id.")
    ax.set_xlabel("dis. (mm)", labelpad=2)
    ax.set_ylabel("force (N)", labelpad=2)
    panel_label(ax, "(c)")
    style_axes(ax, grid=True)
    safe_legend(ax, loc="upper left")

    ax = axes[1, 1]
    labels = ["damp.", "stiff.", "cubic", "force"]
    x = np.arange(len(labels))
    width = 0.36
    ax.bar(x - width / 2, true_params[:4], width=width, color="#D8E8F3", edgecolor="black", linewidth=0.55, label="true")
    ax.bar(x + width / 2, identified[:4], width=width, color=SCI_PALETTE["proposed"], edgecolor="black", linewidth=0.55, label="id.")
    ax.set_xticks(x, labels)
    ax.set_ylabel("coef. value", labelpad=2)
    panel_label(ax, "(d)")
    style_axes(ax, grid=True)
    ax.grid(axis="x", visible=False)
    safe_legend(ax, loc="upper left", ncol=2)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_duffing_identification", out_dir=out_dir, formats=("png",), pad_inches=0.05)
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
