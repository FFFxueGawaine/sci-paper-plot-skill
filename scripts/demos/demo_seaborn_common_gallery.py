# -*- coding: utf-8 -*-
"""Demo 29: common Seaborn plot types adapted to the MSSP SCI style."""

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
import pandas as pd
import seaborn as sns

from scimplstyle_mssp import SCI_PALETTE, apply_sci_style, figure_size, panel_label, save_figure, style_axes


METHODS = ["N4SID", "LSTM", "Proposed"]
PALETTE = {
    "N4SID": SCI_PALETTE["reference"],
    "LSTM": SCI_PALETTE["baseline"],
    "Proposed": SCI_PALETTE["proposed"],
}
LOADS = ["low", "mid", "high"]


def set_seaborn_style() -> None:
    """Keep Seaborn convenient while preserving the compact manuscript style."""
    sns.set_theme(
        context="paper",
        style="ticks",
        font="Times New Roman",
        rc={
            "axes.linewidth": 0.65,
            "axes.labelsize": 8,
            "axes.titlesize": 8,
            "legend.fontsize": 7,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
        },
    )
    sns.set_palette([PALETTE[name] for name in METHODS])


def make_line_data(rng: np.random.Generator) -> pd.DataFrame:
    time = np.linspace(0.0, 2.0, 70)
    rows: list[dict[str, float | int | str]] = []
    settings = {
        "N4SID": (0.42, 1.05, 0.045),
        "LSTM": (0.36, 1.08, 0.030),
        "Proposed": (0.30, 1.10, 0.018),
    }
    for method in METHODS:
        damping, freq, noise = settings[method]
        for load_i, load in enumerate(LOADS):
            load_scale = 1.0 + 0.12 * load_i
            for trial in range(5):
                phase = rng.normal(0.0, 0.045)
                response = load_scale * np.exp(-damping * time) * np.sin(2.0 * np.pi * freq * time + phase)
                response += rng.normal(0.0, noise, time.size)
                for t_i, y_i in zip(time, response):
                    rows.append({"time": t_i, "response": y_i, "method": method, "load": load, "trial": trial})
    return pd.DataFrame(rows)


def make_scatter_data(rng: np.random.Generator) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    slopes = {"N4SID": 0.62, "LSTM": 0.78, "Proposed": 0.92}
    noise = {"N4SID": 0.42, "LSTM": 0.32, "Proposed": 0.22}
    for method in METHODS:
        feature = rng.normal(0.0, 1.0, 85)
        target = slopes[method] * feature + rng.normal(0.0, noise[method], feature.size)
        for x_i, y_i in zip(feature, target):
            rows.append({"feature": x_i, "target": y_i, "method": method})
    return pd.DataFrame(rows)


def make_error_data(rng: np.random.Generator) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    centers = {"N4SID": -0.012, "LSTM": 0.006, "Proposed": 0.000}
    scales = {"N4SID": 0.046, "LSTM": 0.032, "Proposed": 0.019}
    for method in METHODS:
        for load_i, load in enumerate(LOADS):
            values = rng.normal(centers[method] + 0.004 * load_i, scales[method] * (1.0 + 0.12 * load_i), 80)
            for err in values:
                rows.append({"method": method, "load": load, "error": err, "abs_error": abs(err)})
    return pd.DataFrame(rows)


def make_category_data(error_df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    summary = (
        error_df.groupby(["method", "load"], as_index=False)
        .agg(rmse=("error", lambda s: float(np.sqrt(np.mean(np.asarray(s) ** 2)))))
        .reset_index(drop=True)
    )
    rows: list[dict[str, float | str]] = []
    for _, row in summary.iterrows():
        for repeat in range(6):
            rows.append(
                {
                    "method": row["method"],
                    "load": row["load"],
                    "rmse": max(0.0, float(row["rmse"]) + rng.normal(0.0, 0.003)),
                    "trial": f"T{repeat + 1}",
                }
            )
    return pd.DataFrame(rows)


def make_matrix_data(rng: np.random.Generator) -> pd.DataFrame:
    base = rng.normal(size=(180, 5))
    matrix = np.column_stack(
        [
            base[:, 0],
            0.62 * base[:, 0] + 0.45 * base[:, 1],
            -0.36 * base[:, 0] + 0.70 * base[:, 2],
            0.30 * base[:, 1] + 0.60 * base[:, 3],
            -0.24 * base[:, 2] + 0.80 * base[:, 4],
        ]
    )
    return pd.DataFrame(matrix, columns=["gap", "stiff.", "damp.", "speed", "error"])


def save_grid(grid: sns.axisgrid.FacetGrid, name: str, out_dir: Path) -> None:
    for ax in grid.axes.flat:
        if ax is None:
            continue
        style_axes(ax, grid=True)
    grid.savefig(out_dir / f"{name}.png", dpi=600, bbox_inches="tight", pad_inches=0.04)
    plt.close(grid.figure)


def plot_relational_gallery(line_df: pd.DataFrame, scatter_df: pd.DataFrame, out_dir: Path) -> None:
    reg_df = scatter_df[scatter_df["method"] == "Proposed"].copy()
    reg_df["prediction"] = 0.10 + 0.88 * reg_df["feature"] + 0.22 * np.sin(reg_df["feature"])

    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.72), constrained_layout=True)
    sns.scatterplot(data=scatter_df, x="feature", y="target", hue="method", hue_order=METHODS, palette=PALETTE, s=18, linewidth=0.25, ax=axes[0, 0])
    axes[0, 0].set_xlabel("feature 1", labelpad=2)
    axes[0, 0].set_ylabel("target", labelpad=2)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0], grid=True)

    sns.lineplot(
        data=line_df[line_df["load"] == "mid"],
        x="time",
        y="response",
        hue="method",
        hue_order=METHODS,
        palette=PALETTE,
        errorbar="sd",
        linewidth=1.15,
        ax=axes[0, 1],
    )
    axes[0, 1].set_xlabel("time (s)", labelpad=2)
    axes[0, 1].set_ylabel("dis. (mm)", labelpad=2)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1], grid=True)

    sns.regplot(data=reg_df, x="feature", y="prediction", color=SCI_PALETTE["baseline"], scatter_kws={"s": 16}, ax=axes[1, 0])
    axes[1, 0].set_xlabel("feature 1", labelpad=2)
    axes[1, 0].set_ylabel("prediction", labelpad=2)
    panel_label(axes[1, 0], "(c)")
    style_axes(axes[1, 0], grid=True)

    sns.residplot(data=reg_df, x="feature", y="prediction", color=SCI_PALETTE["proposed"], scatter_kws={"s": 16}, ax=axes[1, 1])
    axes[1, 1].axhline(0.0, color=SCI_PALETTE["reference"], linewidth=0.8, linestyle="--")
    axes[1, 1].set_xlabel("feature 1", labelpad=2)
    axes[1, 1].set_ylabel("residual", labelpad=2)
    panel_label(axes[1, 1], "(d)")
    style_axes(axes[1, 1], grid=True)

    for ax in axes.flat:
        legend = ax.get_legend()
        if legend is not None:
            legend.set_title("")
            legend.get_frame().set_linewidth(0.4)
            legend.get_frame().set_alpha(0.92)
    save_figure(fig, "demo_seaborn_relational_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)


def plot_distribution_gallery(error_df: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=figure_size("double", 0.72), constrained_layout=True)
    sns.histplot(data=error_df, x="error", hue="method", hue_order=METHODS, palette=PALETTE, bins=24, stat="density", element="step", common_norm=False, ax=axes[0, 0])
    axes[0, 0].set_xlabel("error (mm)", labelpad=2)
    axes[0, 0].set_ylabel("density", labelpad=2)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0], grid=True)

    sns.kdeplot(data=error_df, x="error", hue="method", hue_order=METHODS, palette=PALETTE, common_norm=False, linewidth=1.2, fill=False, ax=axes[0, 1])
    axes[0, 1].set_xlabel("error (mm)", labelpad=2)
    axes[0, 1].set_ylabel("density", labelpad=2)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1], grid=True)

    sns.ecdfplot(data=error_df, x="abs_error", hue="method", hue_order=METHODS, palette=PALETTE, linewidth=1.15, ax=axes[1, 0])
    axes[1, 0].set_xlabel("abs. error (mm)", labelpad=2)
    axes[1, 0].set_ylabel("cumulative prob.", labelpad=2)
    panel_label(axes[1, 0], "(c)")
    style_axes(axes[1, 0], grid=True)

    subset = error_df[error_df["method"] == "Proposed"]
    sns.kdeplot(data=subset, x="error", color=SCI_PALETTE["proposed"], linewidth=1.2, ax=axes[1, 1])
    sns.rugplot(data=subset.sample(80, random_state=3), x="error", color=SCI_PALETTE["reference"], height=0.08, linewidth=0.55, ax=axes[1, 1])
    axes[1, 1].set_xlabel("error (mm)", labelpad=2)
    axes[1, 1].set_ylabel("density", labelpad=2)
    panel_label(axes[1, 1], "(d)")
    style_axes(axes[1, 1], grid=True)

    for ax in axes.flat:
        legend = ax.get_legend()
        if legend is not None:
            legend.set_title("")
            legend.get_frame().set_linewidth(0.4)
            legend.get_frame().set_alpha(0.92)
    save_figure(fig, "demo_seaborn_distribution_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)


def plot_categorical_gallery(error_df: pd.DataFrame, category_df: pd.DataFrame, out_dir: Path) -> None:
    small_error = error_df.groupby(["method", "load"], group_keys=False).sample(24, random_state=5)
    count_df = pd.DataFrame(
        {
            "fault": ["normal", "rub", "misalign", "rub", "normal", "rub", "misalign", "normal", "rub"] * 5,
            "severity": ["low", "mid", "high", "mid", "low", "high", "mid", "low", "high"] * 5,
        }
    )

    fig, axes = plt.subplots(2, 3, figsize=figure_size("double", 0.78), constrained_layout=True)
    sns.boxplot(data=error_df, x="method", y="error", order=METHODS, hue="method", hue_order=METHODS, palette=PALETTE, dodge=False, showfliers=False, ax=axes[0, 0])
    axes[0, 0].set_xlabel("")
    axes[0, 0].set_ylabel("error (mm)", labelpad=2)
    panel_label(axes[0, 0], "(a)")
    style_axes(axes[0, 0], grid=True)

    sns.violinplot(data=small_error, x="method", y="error", order=METHODS, hue="method", hue_order=METHODS, palette=PALETTE, dodge=False, inner=None, linewidth=0.65, ax=axes[0, 1])
    sns.stripplot(data=small_error, x="method", y="error", order=METHODS, color="black", size=1.7, alpha=0.45, jitter=0.17, ax=axes[0, 1])
    axes[0, 1].set_xlabel("")
    axes[0, 1].set_ylabel("error (mm)", labelpad=2)
    panel_label(axes[0, 1], "(b)")
    style_axes(axes[0, 1], grid=True)

    sns.barplot(data=category_df, x="method", y="rmse", order=METHODS, hue="method", hue_order=METHODS, palette=PALETTE, dodge=False, errorbar="sd", capsize=0.16, ax=axes[0, 2])
    axes[0, 2].set_xlabel("")
    axes[0, 2].set_ylabel("RMSE (mm)", labelpad=2)
    panel_label(axes[0, 2], "(c)")
    style_axes(axes[0, 2], grid=True)

    sns.pointplot(data=category_df, x="load", y="rmse", order=LOADS, hue="method", hue_order=METHODS, palette=PALETTE, errorbar="sd", markers=["o", "s", "^"], linewidth=1.0, ax=axes[1, 0])
    axes[1, 0].set_xlabel("load", labelpad=2)
    axes[1, 0].set_ylabel("RMSE (mm)", labelpad=2)
    panel_label(axes[1, 0], "(d)")
    style_axes(axes[1, 0], grid=True)

    sns.countplot(data=count_df, x="fault", hue="severity", palette=["#D8E8F3", "#BFD9EA", "#F6C8C4"], ax=axes[1, 1])
    axes[1, 1].set_xlabel("fault type", labelpad=2)
    axes[1, 1].set_ylabel("count", labelpad=2)
    panel_label(axes[1, 1], "(e)")
    style_axes(axes[1, 1], grid=True)

    sns.swarmplot(data=small_error, x="load", y="abs_error", order=LOADS, hue="method", hue_order=METHODS, palette=PALETTE, size=2.4, dodge=True, ax=axes[1, 2])
    axes[1, 2].set_xlabel("load", labelpad=2)
    axes[1, 2].set_ylabel("abs. error (mm)", labelpad=2)
    panel_label(axes[1, 2], "(f)")
    style_axes(axes[1, 2], grid=True)

    for ax in axes.flat:
        ax.grid(axis="x", visible=False)
        legend = ax.get_legend()
        if legend is not None:
            legend.set_title("")
            legend.get_frame().set_linewidth(0.4)
            legend.get_frame().set_alpha(0.92)
    save_figure(fig, "demo_seaborn_categorical_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)


def plot_matrix_gallery(matrix_df: pd.DataFrame, out_dir: Path) -> None:
    corr = matrix_df.corr()
    fig, ax = plt.subplots(figsize=figure_size("single", 0.84), constrained_layout=True)
    sns.heatmap(corr, vmin=-1.0, vmax=1.0, cmap="vlag", square=True, linewidths=0.45, linecolor="white", cbar_kws={"label": "corr."}, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(length=0)
    panel_label(ax, "(a)")
    save_figure(fig, "demo_seaborn_heatmap_gallery", out_dir=out_dir, formats=("png",))
    plt.close(fig)


def plot_figure_level_galleries(line_df: pd.DataFrame, error_df: pd.DataFrame, category_df: pd.DataFrame, matrix_df: pd.DataFrame, out_dir: Path) -> None:
    pair_df = matrix_df.sample(110, random_state=8).copy()
    pair_df["method"] = np.resize(METHODS, pair_df.shape[0])
    pair_grid = sns.pairplot(pair_df, vars=["gap", "stiff.", "damp.", "error"], hue="method", hue_order=METHODS, palette=PALETTE, corner=True, plot_kws={"s": 11, "linewidth": 0.15})
    pair_grid.figure.set_size_inches(*figure_size("double", 0.74))
    save_grid(pair_grid, "demo_seaborn_pairplot_gallery", out_dir)

    rel_grid = sns.relplot(
        data=line_df,
        x="time",
        y="response",
        hue="method",
        hue_order=METHODS,
        col="load",
        col_order=LOADS,
        kind="line",
        palette=PALETTE,
        errorbar="sd",
        linewidth=1.05,
        height=2.0,
        aspect=1.0,
    )
    rel_grid.figure.set_size_inches(*figure_size("double", 0.36))
    rel_grid.set_axis_labels("time (s)", "dis. (mm)")
    save_grid(rel_grid, "demo_seaborn_relplot_gallery", out_dir)

    cat_grid = sns.catplot(
        data=category_df,
        x="load",
        y="rmse",
        order=LOADS,
        hue="method",
        hue_order=METHODS,
        col="method",
        col_order=METHODS,
        kind="bar",
        palette=PALETTE,
        errorbar="sd",
        height=2.0,
        aspect=0.9,
    )
    cat_grid.figure.set_size_inches(*figure_size("double", 0.35))
    cat_grid.set_axis_labels("load", "RMSE (mm)")
    save_grid(cat_grid, "demo_seaborn_catplot_gallery", out_dir)

    dis_grid = sns.displot(
        data=error_df,
        x="error",
        hue="method",
        hue_order=METHODS,
        col="load",
        col_order=LOADS,
        kind="kde",
        palette=PALETTE,
        common_norm=False,
        linewidth=1.05,
        height=2.0,
        aspect=0.9,
    )
    dis_grid.figure.set_size_inches(*figure_size("double", 0.35))
    dis_grid.set_axis_labels("error (mm)", "density")
    save_grid(dis_grid, "demo_seaborn_displot_gallery", out_dir)


def main() -> None:
    apply_sci_style(base_size=8)
    set_seaborn_style()
    rng = np.random.default_rng(20260521)
    line_df = make_line_data(rng)
    scatter_df = make_scatter_data(rng)
    error_df = make_error_data(rng)
    category_df = make_category_data(error_df, rng)
    matrix_df = make_matrix_data(rng)

    out_dir = Path(__file__).resolve().parent / "output"
    plot_relational_gallery(line_df, scatter_df, out_dir)
    plot_distribution_gallery(error_df, out_dir)
    plot_categorical_gallery(error_df, category_df, out_dir)
    plot_matrix_gallery(matrix_df, out_dir)
    plot_figure_level_galleries(line_df, error_df, category_df, matrix_df, out_dir)
    print(out_dir)


if __name__ == "__main__":
    main()
