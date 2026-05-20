# -*- coding: utf-8 -*-
"""Demo 25: common nonlinear systems gallery for dynamics papers."""

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


def rk4(rhs, state: np.ndarray, time: float, dt: float) -> np.ndarray:
    k1 = rhs(state, time)
    k2 = rhs(state + 0.5 * dt * k1, time + 0.5 * dt)
    k3 = rhs(state + 0.5 * dt * k2, time + 0.5 * dt)
    k4 = rhs(state + dt * k3, time + dt)
    return state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def integrate(rhs, initial: tuple[float, float], dt: float, end: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    time = np.arange(0.0, end + dt, dt)
    state = np.zeros((time.size, 2))
    state[0] = np.array(initial)
    for i in range(1, time.size):
        state[i] = rk4(rhs, state[i - 1], time[i - 1], dt)
    return time, state[:, 0], state[:, 1]


def bouc_wen_loop() -> tuple[np.ndarray, np.ndarray]:
    time = np.linspace(0.0, 5.0, 3000)
    dt = time[1] - time[0]
    dis = 1.0 * np.sin(2 * np.pi * 1.2 * time)
    vel = np.gradient(dis, dt)
    z = np.zeros_like(time)
    for i in range(1, time.size):
        dz = 1.15 * vel[i - 1] - 0.62 * abs(vel[i - 1]) * z[i - 1] - 0.18 * vel[i - 1] * abs(z[i - 1])
        z[i] = z[i - 1] + dt * dz
    force = 0.55 * dis + 0.95 * z
    return dis, force


def system_label(ax, text: str) -> None:
    ax.text(0.04, 0.94, text, transform=ax.transAxes, ha="left", va="top", fontsize=8)


def main() -> None:
    apply_sci_style(base_size=8)

    duff_rhs = lambda y, t: np.array([y[1], 0.30 * np.cos(1.05 * t) - 0.07 * y[1] - y[0] - 0.85 * y[0] ** 3])
    vdp_rhs = lambda y, t: np.array([y[1], 1.35 * (1 - y[0] ** 2) * y[1] - y[0]])
    pend_rhs = lambda y, t: np.array([y[1], -0.10 * y[1] - np.sin(y[0])])

    _, duff_x, duff_v = integrate(duff_rhs, (0.12, 0.0), 0.006, 36.0)
    _, vdp_x, vdp_v = integrate(vdp_rhs, (1.25, 0.1), 0.006, 32.0)
    _, pend_x, pend_v = integrate(pend_rhs, (2.45, 0.0), 0.006, 26.0)
    bw_x, bw_f = bouc_wen_loop()

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.58), constrained_layout=True)
    panels = axes.ravel()

    panels[0].plot(duff_x[-3300:], duff_v[-3300:], color=SCI_PALETTE["experiment"], lw=0.55)
    panels[0].set_xlabel("dis. (mm)", labelpad=2)
    panels[0].set_ylabel("vel. (mm/s)", labelpad=2)
    system_label(panels[0], "Duffing")

    panels[1].plot(vdp_x[-3800:], vdp_v[-3800:], color=SCI_PALETTE["baseline"], lw=0.60)
    panels[1].set_xlabel("state (-)", labelpad=2)
    panels[1].set_ylabel("vel. (-)", labelpad=2)
    system_label(panels[1], "Van der Pol")

    panels[2].plot(pend_x, pend_v, color=SCI_PALETTE["reference"], lw=0.65)
    panels[2].set_xlabel("angle (rad)", labelpad=2)
    panels[2].set_ylabel("ang. vel. (rad/s)", labelpad=2)
    system_label(panels[2], "pendulum")

    panels[3].plot(bw_x[-1800:], bw_f[-1800:], color=SCI_PALETTE["proposed"], lw=0.80)
    panels[3].set_xlabel("dis. (mm)", labelpad=2)
    panels[3].set_ylabel("force (N)", labelpad=2)
    system_label(panels[3], "Bouc-Wen")

    for label, ax in zip(["(a)", "(b)", "(c)", "(d)"], panels):
        panel_label(ax, label)
        style_axes(ax, grid=True)

    out_dir = Path(__file__).resolve().parent / "output"
    save_figure(fig, "demo_nonlinear_systems_gallery", out_dir=out_dir, formats=("png",), pad_inches=0.05)
    plt.close(fig)
    print(out_dir)


if __name__ == "__main__":
    main()
