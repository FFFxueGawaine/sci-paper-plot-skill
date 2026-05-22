# -*- coding: utf-8 -*-
"""Figure templates for the hierarchical Bayesian clearance-system paper."""

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
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
import numpy as np

from scimplstyle_mssp import (
    SCI_PALETTE,
    add_zoom_inset,
    apply_sci_style,
    figure_size,
    panel_label,
    safe_legend,
    save_figure,
    style_axes,
)


BLUE = SCI_PALETTE["baseline"]
RED = SCI_PALETTE["identified"]
BLACK = SCI_PALETTE["experiment"]
GRAY = SCI_PALETTE["reference"]


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2.0 * np.pi))


def active_stem(ax: object, labels: list[str], values: np.ndarray, threshold: float = 0.45) -> None:
    x = np.arange(len(labels))
    markerline, stemlines, baseline = ax.stem(x, values, basefmt=" ", linefmt=BLUE, markerfmt="o")
    markerline.set_markerfacecolor(BLUE)
    markerline.set_markeredgecolor(BLUE)
    markerline.set_markersize(3.2)
    stemlines.set_linewidth(0.8)
    active = values >= threshold
    ax.scatter(x[active], values[active], s=20, color=RED, zorder=4, label="active")
    ax.axhline(threshold, color="0.55", linestyle="--", linewidth=0.8, label="threshold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=55, ha="right")
    ax.set_ylabel("prob. (-)")
    ax.set_ylim(-0.04, 1.12)
    style_axes(ax, grid=True)


def shaded_group(ax: object, start: float, end: float, label: str, color: str = "0.93") -> None:
    ax.axvspan(start - 0.5, end + 0.5, color=color, zorder=-5)
    ax.text((start + end) / 2, 0.04, label, ha="center", va="bottom", fontsize=7, color="0.35")


def add_arrow(ax: object, xy1: tuple[float, float], xy2: tuple[float, float]) -> None:
    arrow = FancyArrowPatch(xy1, xy2, arrowstyle="-|>", mutation_scale=10, lw=0.9, color="0.35")
    ax.add_patch(arrow)


def template_fig001_bayesian_workflow(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    fig, ax = plt.subplots(figsize=figure_size("double", 0.32), constrained_layout=True)
    ax.set_axis_off()
    boxes = [
        (0.03, 0.35, 0.14, 0.30, "response\nx, v, a"),
        (0.23, 0.35, 0.16, 0.30, "candidate\nlibrary"),
        (0.46, 0.35, 0.16, 0.30, "sparse\nprior"),
        (0.69, 0.35, 0.13, 0.30, "posterior\nmodel"),
        (0.88, 0.35, 0.10, 0.30, "validation"),
    ]
    for x, y, w, h, text in boxes:
        ax.add_patch(Rectangle((x, y), w, h, transform=ax.transAxes, ec="0.25", fc="0.96", lw=0.9))
        ax.text(x + w / 2, y + h / 2, text, transform=ax.transAxes, ha="center", va="center")
    for i in range(len(boxes) - 1):
        x, y, w, h, _ = boxes[i]
        nx, ny, _, nh, _ = boxes[i + 1]
        add_arrow(ax, (x + w + 0.01, y + h / 2), (nx - 0.01, ny + nh / 2))
    ax.text(0.46, 0.15, "clearance prior + spike-and-slab model selection", transform=ax.transAxes, ha="center")
    save_figure(fig, "Fig.001_bayesian_workflow_template", out_dir=out_dir)
    plt.close(fig)


def template_fig002_clearance_basis(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    x = np.linspace(-3.0, 3.0, 500)
    delta_neg, delta_pos = -0.9, 1.1
    h_neg = np.maximum(delta_neg - x, 0.0)
    h_pos = np.maximum(x - delta_pos, 0.0)
    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.38), constrained_layout=True)
    axes[0].plot(x, h_neg, color=BLUE, label="negative contact")
    axes[0].plot(x, h_pos, color=RED, label="positive contact")
    axes[0].axvspan(delta_neg, delta_pos, color="0.92", label="free zone")
    axes[0].axvline(delta_neg, color="0.45", ls="--", lw=0.8)
    axes[0].axvline(delta_pos, color="0.45", ls="--", lw=0.8)
    axes[0].set_xlabel("dis. (mm)")
    axes[0].set_ylabel("basis amp. (-)")
    panel_label(axes[0], "(a)")
    safe_legend(axes[0], loc="upper center", ncol=2)
    style_axes(axes[0], grid=True)
    force = 0.15 * x + 2.4 * h_pos - 1.8 * h_neg
    axes[1].plot(x, force, color=BLACK, lw=1.3)
    axes[1].axvline(delta_neg, color=BLUE, ls="--", lw=0.8)
    axes[1].axvline(delta_pos, color=RED, ls="--", lw=0.8)
    axes[1].set_xlabel("dis. (mm)")
    axes[1].set_ylabel("force (N)")
    panel_label(axes[1], "(b)")
    style_axes(axes[1], grid=True)
    save_figure(fig, "Fig.002_clearance_basis_template", out_dir=out_dir)
    plt.close(fig)


def template_fig003_one_sided_impact(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    fig, ax = plt.subplots(figsize=figure_size("single", 0.70), constrained_layout=True)
    ax.set_axis_off()
    ax.add_patch(Rectangle((0.12, 0.43), 0.22, 0.16, transform=ax.transAxes, ec=BLACK, fc="0.93", lw=1.1))
    ax.text(0.23, 0.51, "m", transform=ax.transAxes, ha="center", va="center", fontsize=12)
    ax.plot([0.34, 0.58], [0.51, 0.51], transform=ax.transAxes, color=BLACK, lw=1.1)
    for x0 in np.linspace(0.36, 0.55, 6):
        ax.plot([x0, x0 + 0.015], [0.48, 0.54], transform=ax.transAxes, color=BLACK, lw=0.8)
    ax.add_patch(Rectangle((0.67, 0.33), 0.035, 0.36, transform=ax.transAxes, ec=RED, fc="0.92", lw=1.1))
    ax.text(0.74, 0.66, "stop", transform=ax.transAxes, color=RED, ha="left")
    ax.annotate("", xy=(0.67, 0.38), xytext=(0.58, 0.38), xycoords=ax.transAxes, arrowprops={"arrowstyle": "<->", "lw": 0.8})
    ax.text(0.625, 0.33, "clearance", transform=ax.transAxes, ha="center", va="top")
    ax.text(0.18, 0.31, "spring-damper support", transform=ax.transAxes, ha="left")
    save_figure(fig, "Fig.003_one_sided_impact_template", out_dir=out_dir)
    plt.close(fig)


def template_fig004_ppc_kde(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    rng = np.random.default_rng(4)
    fig, axes = plt.subplots(1, 3, figsize=figure_size("double", 0.34), constrained_layout=True)
    x = np.linspace(-2.2, 2.2, 400)
    for i, ax in enumerate(axes):
        obs = normal_pdf(x, 0.18 * i - 0.1, 0.45 + 0.04 * i) + 0.28 * normal_pdf(x, 1.05, 0.22)
        ax.plot(x, obs, color=BLACK, lw=1.4, label="experiment")
        for _ in range(9):
            mu = 0.18 * i - 0.1 + rng.normal(0, 0.05)
            sd = 0.45 + 0.04 * i + rng.normal(0, 0.015)
            pred = normal_pdf(x, mu, sd) + 0.28 * normal_pdf(x, 1.05 + rng.normal(0, 0.04), 0.23)
            ax.plot(x, pred, color=RED, lw=0.7, alpha=0.35)
        ax.set_xlabel(r"$y$")
        ax.set_ylabel("KDE")
        ax.text(0.06, 0.84, r"$R^2=0.99$", transform=ax.transAxes, fontsize=8)
        panel_label(ax, f"({chr(97+i)})")
        style_axes(ax)
    safe_legend(axes[0], loc="upper left")
    save_figure(fig, "Fig.004_ppc_kde_template", out_dir=out_dir)
    plt.close(fig)


def template_fig005_library_selection(out_dir: Path) -> None:
    apply_sci_style(base_size=8)
    labels = [r"$1$", r"$x$", r"$v$", r"$x^2$", r"$xv$", r"$v^2$", r"$H_-x$", r"$H_-v$", r"$H_+x$", r"$H_+v$", r"$x^3$", r"$v^3$"]
    values = np.array([0.03, 0.98, 0.07, 0.04, 0.05, 0.02, 0.96, 0.88, 0.93, 0.90, 0.03, 0.02])
    fig, ax = plt.subplots(figsize=figure_size("double", 0.32), constrained_layout=True)
    shaded_group(ax, 0, 5, "linear/candidate terms")
    shaded_group(ax, 6, 9, "clearance terms", color="#eef4fb")
    active_stem(ax, labels, values)
    panel_label(ax, "(a)")
    safe_legend(ax, loc="upper center", ncol=2)
    save_figure(fig, "Fig.005_library_selection_template", out_dir=out_dir)
    plt.close(fig)


def template_fig006_posterior_density_grid(out_dir: Path) -> None:
    apply_sci_style(base_size=8)
    fig, axes = plt.subplots(2, 3, figsize=figure_size("double", 0.48), constrained_layout=True)
    x = np.linspace(-3.0, 3.0, 500)
    params = [
        (1.0, 0.10, r"$1/m$"),
        (0.0, 0.28, r"$k_1/m$"),
        (1.4, 0.18, r"$c_1/m$"),
        (-1.1, 0.22, r"$k_2/m$"),
        (0.75, 0.16, r"$c_2/m$"),
        (0.15, 0.08, r"$\delta$"),
    ]
    for i, (ax, (mu, sd, label)) in enumerate(zip(axes.flat, params)):
        y = normal_pdf(x, mu, sd)
        ax.fill_between(x, y, color=BLUE, alpha=0.35)
        ax.plot(x, y, color=BLUE, lw=1.0)
        ax.axvline(mu, color=RED, ls="--", lw=0.9)
        ax.text(0.05, 0.85, label, transform=ax.transAxes)
        panel_label(ax, f"({chr(97+i)})")
        ax.set_xlabel("value")
        ax.set_ylabel("density")
        style_axes(ax)
    save_figure(fig, "Fig.006_posterior_density_grid_template", out_dir=out_dir)
    plt.close(fig)


def template_fig007_tristable_nes_schematic(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    fig, axes = plt.subplots(1, 3, figsize=figure_size("double", 0.34), constrained_layout=True)
    for i, ax in enumerate(axes):
        ax.set_axis_off()
        panel_label(ax, f"({chr(97+i)})")
        ax.plot([0.10, 0.90], [0.50, 0.50], color=BLACK, lw=1.0, transform=ax.transAxes)
        ax.add_patch(Rectangle((0.42 + 0.07 * i, 0.28), 0.10, 0.44, transform=ax.transAxes, ec=BLACK, fc="0.95"))
        for x, color in [(0.24, BLUE), (0.76, RED)]:
            ax.add_patch(Rectangle((x, 0.25), 0.08, 0.50, transform=ax.transAxes, ec=color, fc=color, alpha=0.78))
        ax.text(0.50, 0.12, f"gap state {i+1}", transform=ax.transAxes, ha="center")
    save_figure(fig, "Fig.007_tristable_nes_schematic_template", out_dir=out_dir)
    plt.close(fig)


def template_fig008_piecewise_force(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    d = np.linspace(-3.0, 3.0, 500)
    force = np.piecewise(d, [d < -1.0, (d >= -1.0) & (d <= 1.0), d > 1.0], [lambda z: -15 * (z + 1), lambda z: 0.5 * z, lambda z: 14 * (z - 1)])
    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.38), constrained_layout=True)
    axes[0].plot(d, force, color=BLACK, lw=1.3)
    axes[0].axvline(-1, color=BLUE, ls="--", lw=0.8)
    axes[0].axvline(1, color=RED, ls="--", lw=0.8)
    axes[0].set_xlabel("dis. (mm)")
    axes[0].set_ylabel("force (N)")
    panel_label(axes[0], "(a)")
    style_axes(axes[0], grid=True)
    axes[1].plot(d, np.maximum(-1 - d, 0), color=BLUE, label="left basis")
    axes[1].plot(d, np.maximum(d - 1, 0), color=RED, label="right basis")
    axes[1].plot(d, 0.5 * d, color=GRAY, ls="--", label="linear")
    axes[1].set_xlabel("dis. (mm)")
    axes[1].set_ylabel("basis value (-)")
    panel_label(axes[1], "(b)")
    style_axes(axes[1], grid=True)
    safe_legend(axes[1], loc="upper center", ncol=1)
    save_figure(fig, "Fig.008_piecewise_force_template", out_dir=out_dir)
    plt.close(fig)


def template_fig009_library_selection_tristable(out_dir: Path) -> None:
    apply_sci_style(base_size=8)
    labels = [r"$x_1$", r"$v_1$", r"$x_2$", r"$v_2$", r"$H_1$", r"$H_2$", r"$H_3$", r"$H_4$", r"$x^2$", r"$x^3$"]
    values = np.array([0.99, 0.05, 0.91, 0.08, 0.02, 0.84, 0.79, 0.04, 0.03, 0.02])
    fig, ax = plt.subplots(figsize=figure_size("double", 0.30), constrained_layout=True)
    shaded_group(ax, 0, 3, "linear terms")
    shaded_group(ax, 4, 7, "clearance terms", color="#eef4fb")
    active_stem(ax, labels, values, threshold=0.5)
    safe_legend(ax, loc="upper right")
    save_figure(fig, "Fig.009_library_selection_tristable_template", out_dir=out_dir)
    plt.close(fig)


def template_fig010_density_triplet(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    fig, axes = plt.subplots(1, 3, figsize=figure_size("double", 0.30), constrained_layout=True)
    centers = [1.0, 3.0, 0.55]
    labels = [r"$1/m$", r"$k/m$", r"$c/m$"]
    for i, ax in enumerate(axes):
        x = np.linspace(centers[i] - 0.6, centers[i] + 0.6, 400)
        y = normal_pdf(x, centers[i], 0.12 + 0.04 * i)
        ax.fill_between(x, y, color=BLUE, alpha=0.32)
        ax.plot(x, y, color=BLUE)
        ax.axvline(centers[i], color=RED, ls="--", lw=0.9)
        ax.set_xlabel(labels[i])
        ax.set_ylabel("density")
        ax.text(0.06, 0.83, "mean +/- sd", transform=ax.transAxes, fontsize=8)
        panel_label(ax, f"({chr(97+i)})")
        style_axes(ax)
    save_figure(fig, "Fig.010_density_triplet_template", out_dir=out_dir)
    plt.close(fig)


def template_fig011_joint_posterior_scatter(out_dir: Path) -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(11)
    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.64), constrained_layout=True)
    for i, ax in enumerate(axes.flat):
        cov = np.array([[1.0, 0.55 - 0.25 * i], [0.55 - 0.25 * i, 0.7]])
        points = rng.multivariate_normal([0.3 * i, -0.2 * i], cov, size=700)
        color = np.hypot(points[:, 0], points[:, 1])
        sc = ax.scatter(points[:, 0], points[:, 1], c=color, s=5, cmap="magma", alpha=0.55, linewidths=0)
        ax.set_xlabel(r"$\theta_1$")
        ax.set_ylabel(r"$\theta_2$")
        panel_label(ax, f"({chr(97+i)})")
        style_axes(ax)
    fig.colorbar(sc, ax=axes, shrink=0.74, label="density proxy (-)")
    save_figure(fig, "Fig.011_joint_posterior_scatter_template", out_dir=out_dir)
    plt.close(fig)


def template_fig012_validation_timeseries(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    t = np.linspace(0, 4.0, 900)
    fig, axes = plt.subplots(1, 3, figsize=figure_size("double", 0.30), sharex=True, constrained_layout=True)
    for i, ax in enumerate(axes):
        truth = np.sin(2 * np.pi * (1.2 + 0.3 * i) * t) * np.exp(-0.08 * t)
        pred = truth + 0.08 * np.sin(2 * np.pi * 0.45 * t + i)
        band = 0.10 + 0.02 * i
        ax.fill_between(t, pred - band, pred + band, color=RED, alpha=0.12, linewidth=0)
        ax.plot(t, truth, color=BLACK, lw=1.0, label="experiment")
        ax.plot(t, pred, color=RED, ls="--", lw=1.0, label="identified")
        ax.set_xlabel("time (s)")
        if i == 0:
            ax.set_ylabel(r"$y$ (m/s$^2$)")
        panel_label(ax, f"({chr(97+i)})")
        style_axes(ax, grid=True)
    safe_legend(axes[0], loc="upper right")
    save_figure(fig, "Fig.012_validation_timeseries_template", out_dir=out_dir)
    plt.close(fig)


def template_fig013_experimental_setup(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    fig, ax = plt.subplots(figsize=figure_size("double", 0.30), constrained_layout=True)
    ax.set_axis_off()
    ax.add_patch(Rectangle((0.08, 0.42), 0.70, 0.06, transform=ax.transAxes, ec=BLACK, fc="0.85", lw=1.0))
    ax.add_patch(Rectangle((0.08, 0.34), 0.05, 0.22, transform=ax.transAxes, ec=BLACK, fc="0.65", lw=1.0))
    ax.add_patch(Rectangle((0.70, 0.50), 0.06, 0.14, transform=ax.transAxes, ec=BLACK, fc="0.75", lw=0.9))
    for x, label in [(0.48, "sensor"), (0.82, "leaf spring stop")]:
        ax.add_patch(Circle((x, 0.54), 0.025, transform=ax.transAxes, ec=RED, fc="white", lw=1.0))
        ax.text(x, 0.68, label, transform=ax.transAxes, ha="center")
    ax.annotate("", xy=(0.80, 0.46), xytext=(0.74, 0.46), xycoords=ax.transAxes, arrowprops={"arrowstyle": "<->", "lw": 0.8})
    ax.text(0.77, 0.36, "clearance", transform=ax.transAxes, ha="center")
    ax.text(0.38, 0.25, "cantilever beam with adjustable bilateral stops", transform=ax.transAxes, ha="center")
    save_figure(fig, "Fig.013_experimental_setup_template", out_dir=out_dir)
    plt.close(fig)


def template_fig014_time_frequency_composite(out_dir: Path) -> None:
    apply_sci_style(base_size=8)
    t = np.linspace(0, 60, 600)
    f = np.linspace(0, 60, 180)
    fig, axes = plt.subplots(2, 3, figsize=figure_size("double", 0.62), constrained_layout=True)
    for i in range(3):
        response = (0.15 + 0.10 * i) * np.sin(2 * np.pi * (0.08 * t + 0.002 * t**2)) * np.exp(-0.006 * t)
        axes[0, i].plot(t, response, color=BLACK, lw=0.8)
        axes[0, i].set_xlabel("time (s)")
        axes[0, i].set_ylabel("dis. (mm)")
        panel_label(axes[0, i], f"({chr(97+i)})")
        style_axes(axes[0, i])
        ridge = 9 + 0.45 * t + i * 5
        z = np.exp(-0.5 * ((f[:, None] - ridge[None, :]) / 2.5) ** 2)
        z += 0.35 * np.exp(-0.5 * ((f[:, None] - (30 + 0.10 * t)[None, :]) / 3.0) ** 2)
        im = axes[1, i].imshow(z, extent=[t.min(), t.max(), f.min(), f.max()], origin="lower", aspect="auto", cmap="viridis")
        axes[1, i].set_xlabel("time (s)")
        axes[1, i].set_ylabel("fre. (Hz)")
        panel_label(axes[1, i], f"({chr(100+i)})")
        style_axes(axes[1, i])
    fig.colorbar(im, ax=axes[:, -1], shrink=0.85, label="energy (-)")
    save_figure(fig, "Fig.014_time_frequency_composite_template", out_dir=out_dir)
    plt.close(fig)


def template_fig015_time_hist_clearance(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    rng = np.random.default_rng(15)
    t = np.linspace(0, 60, 1500)
    x = 0.18 * np.sin(2 * np.pi * 0.55 * t) + 0.05 * np.sin(2 * np.pi * 1.7 * t)
    samples = np.r_[rng.normal(-0.46, 0.035, 900), rng.normal(0.17, 0.025, 600)]
    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.34), constrained_layout=True)
    axes[0].plot(t, x, color=BLACK, lw=0.8)
    axes[0].set_xlabel("time (s)")
    axes[0].set_ylabel("dis. (mm)")
    panel_label(axes[0], "(a)")
    style_axes(axes[0])
    axes[1].hist(samples, bins=60, density=True, color="#9AC16E", edgecolor="white", linewidth=0.2)
    for d, color in [(-0.46, BLUE), (0.17, RED)]:
        axes[1].axvline(d, color=color, ls="--", lw=1.0)
        axes[1].text(d, axes[1].get_ylim()[1] * 0.86, rf"$\delta={d:.2f}$", ha="center", fontsize=8)
    axes[1].set_xlabel("dis. (mm)")
    axes[1].set_ylabel("density")
    panel_label(axes[1], "(b)")
    style_axes(axes[1])
    save_figure(fig, "Fig.015_time_hist_clearance_template", out_dir=out_dir)
    plt.close(fig)


def template_fig016_experimental_joint_posterior(out_dir: Path) -> None:
    apply_sci_style(base_size=8)
    rng = np.random.default_rng(16)
    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.64), constrained_layout=True)
    pairs = [(0.55, 0.18), (-0.40, -0.08), (0.12, 0.45), (-0.25, 0.25)]
    for i, (ax, center) in enumerate(zip(axes.flat, pairs)):
        pts = rng.normal(center, [0.12, 0.05], size=(900, 2))
        c = np.linspace(0, 1, pts.shape[0])
        sc = ax.scatter(pts[:, 0], pts[:, 1], c=c, cmap="viridis", s=5, alpha=0.55, linewidths=0)
        ax.axvline(center[0], color=RED, ls="--", lw=0.8)
        ax.axhline(center[1], color=RED, ls="--", lw=0.8)
        ax.set_xlabel(r"$\theta_i$")
        ax.set_ylabel(r"$\delta_i$")
        panel_label(ax, f"({chr(97+i)})")
        style_axes(ax)
    fig.colorbar(sc, ax=axes, shrink=0.74, label="sample order")
    save_figure(fig, "Fig.016_experimental_joint_posterior_template", out_dir=out_dir)
    plt.close(fig)


def template_fig017_multidof_validation(out_dir: Path) -> None:
    apply_sci_style(base_size=8)
    t = np.linspace(0, 60, 1800)
    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.58), constrained_layout=True)
    for i, ax in enumerate(axes.flat):
        exp = (1.2 + 0.2 * i) * np.sin(2 * np.pi * (0.18 + 0.03 * i) * t) * (1 + 0.18 * np.sin(2 * np.pi * 0.02 * t))
        est = exp + 0.15 * np.sin(2 * np.pi * 0.42 * t + i)
        ax.plot(t, exp, color=BLACK, lw=0.8, label="experiment")
        ax.plot(t, est, color=RED, ls="--", lw=0.8, label="identified")
        ax.axvspan(0, 18, color="0.92", zorder=-5)
        ax.text(0.05, 0.88, "training", transform=ax.transAxes, fontsize=7)
        ax.set_xlabel("time (s)")
        ax.set_ylabel(r"$y$ (m/s$^2$)")
        panel_label(ax, f"({chr(97+i)})")
        style_axes(ax)
        if i in (0, 1):
            inset = add_zoom_inset(ax, xlim=(31, 36), ylim=(-1.5, 1.5), bounds=(0.55, 0.55, 0.36, 0.32), connectors=(1, 3), connector_visible=(False, True))
            inset.plot(t, exp, color=BLACK, lw=0.7)
            inset.plot(t, est, color=RED, ls="--", lw=0.7)
    safe_legend(axes.flat[0], loc="upper right")
    save_figure(fig, "Fig.017_multidof_validation_template", out_dir=out_dir, pad_inches=0.06)
    plt.close(fig)


def template_fig018_force_phase_validation(out_dir: Path) -> None:
    apply_sci_style(base_size=9)
    t = np.linspace(0, 8, 900)
    force = 1.4 * np.sin(2 * np.pi * 1.2 * t) * np.exp(-0.05 * t)
    identified = force + 0.08 * np.sin(2 * np.pi * 3.1 * t)
    x = 0.35 * np.sin(2 * np.pi * 1.2 * t)
    v = np.gradient(x, t)
    fig, axes = plt.subplots(1, 2, figsize=figure_size("double", 0.34), constrained_layout=True)
    axes[0].plot(t, force, color=BLACK, lw=1.0, label="experiment")
    axes[0].plot(t, identified, color=RED, ls="--", lw=1.0, label="identified")
    axes[0].set_xlabel("time (s)")
    axes[0].set_ylabel("force (N)")
    panel_label(axes[0], "(a)")
    style_axes(axes[0], grid=True)
    safe_legend(axes[0], loc="upper right")
    axes[1].plot(x, v, color=BLUE, lw=1.0, label="experiment")
    axes[1].plot(x, v + 0.04 * np.sin(20 * x), color=RED, ls="--", lw=1.0, label="identified")
    axes[1].set_xlabel("dis. (mm)")
    axes[1].set_ylabel("vel. (mm/s)")
    panel_label(axes[1], "(b)")
    style_axes(axes[1], grid=True)
    safe_legend(axes[1], loc="upper right")
    save_figure(fig, "Fig.018_force_phase_validation_template", out_dir=out_dir)
    plt.close(fig)


TEMPLATES = [
    template_fig001_bayesian_workflow,
    template_fig002_clearance_basis,
    template_fig003_one_sided_impact,
    template_fig004_ppc_kde,
    template_fig005_library_selection,
    template_fig006_posterior_density_grid,
    template_fig007_tristable_nes_schematic,
    template_fig008_piecewise_force,
    template_fig009_library_selection_tristable,
    template_fig010_density_triplet,
    template_fig011_joint_posterior_scatter,
    template_fig012_validation_timeseries,
    template_fig013_experimental_setup,
    template_fig014_time_frequency_composite,
    template_fig015_time_hist_clearance,
    template_fig016_experimental_joint_posterior,
    template_fig017_multidof_validation,
    template_fig018_force_phase_validation,
]


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "output" / "hb_clearance_templates"
    for template in TEMPLATES:
        template(out_dir)
    print(out_dir)


if __name__ == "__main__":
    main()
