# -*- coding: utf-8 -*-
"""Reusable Matplotlib style helpers for SCI manuscript figures."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Literal


SCI_PALETTE = {
    "experiment": "#000000",
    "identified": "#E41A1C",
    "proposed": "#E41A1C",
    "baseline": "#377EB8",
    "reference": "#4D4D4D",
    "snr40": "#0033CC",
    "snr30": "#4C86A8",
    "snr20": "#A95C2B",
    "band": "#76B7B2",
}


def mm_to_inch(mm: float) -> float:
    return mm / 25.4


def figure_size(
    width: Literal["single", "double"] | float = "double",
    height_ratio: float = 0.42,
) -> tuple[float, float]:
    """Return figure size in inches from SCI column width presets."""
    width_mm = {"single": 85.0, "double": 178.0}[width] if isinstance(width, str) else width
    width_in = mm_to_inch(width_mm)
    return width_in, width_in * height_ratio


def apply_sci_style(font_family: str = "Times New Roman", base_size: int = 10) -> None:
    """Apply a conservative SCI paper style to Matplotlib."""
    import matplotlib as mpl

    mpl.rcParams.update(
        {
            "font.family": font_family,
            "font.size": base_size,
            "mathtext.fontset": "stix",
            "axes.labelsize": base_size + 1,
            "axes.titlesize": base_size + 1,
            "axes.axisbelow": True,
            "xtick.labelsize": base_size,
            "ytick.labelsize": base_size,
            "legend.fontsize": base_size,
            "axes.linewidth": 0.8,
            "lines.linewidth": 1.4,
            "lines.markersize": 4,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "savefig.dpi": 600,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "grid.color": "0.88",
            "grid.linewidth": 0.35,
            "grid.alpha": 0.55,
            "legend.frameon": True,
            "legend.edgecolor": "0.8",
            "legend.facecolor": "white",
            "legend.framealpha": 0.84,
            "legend.borderaxespad": 0.25,
        }
    )


def panel_label(
    ax: Any,
    label: str,
    x: float = 0.5,
    y: float = 1.04,
    size: int | None = None,
) -> None:
    """Place a bold panel label such as '(a)' above an axes."""
    if size is None:
        import matplotlib as mpl

        size = int(mpl.rcParams.get("font.size", 10)) + 4
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontweight="bold",
        fontsize=size,
    )


def style_axes(ax: Any, grid: bool = False) -> None:
    """Apply consistent ticks and optional light grid to one axes."""
    ax.tick_params(direction="in", top=False, right=False)
    ax.set_axisbelow(True)
    if grid:
        ax.grid(True, color="0.88", linewidth=0.35, alpha=0.55, zorder=0)


def add_zoom_inset(
    ax: Any,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    loc: str = "upper right",
    width: str = "36%",
    height: str = "36%",
    borderpad: float = 1.0,
    connectors: tuple[int, int] = (2, 4),
    grid: bool = True,
    ypad_fraction: float = 0.08,
    tick_side: Literal["auto", "left", "right"] = "auto",
) -> Any:
    """Create a compact local zoom inset and mark its region on the parent axes."""
    import matplotlib as mpl
    from matplotlib.ticker import MaxNLocator
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

    y0, y1 = ylim
    if ypad_fraction > 0:
        ypad = (y1 - y0) * ypad_fraction
        y0 -= ypad
        y1 += ypad

    inset = inset_axes(ax, width=width, height=height, loc=loc, borderpad=borderpad)
    inset.set_xlim(*xlim)
    inset.set_ylim(y0, y1)
    style_axes(inset, grid=grid)
    inset.xaxis.set_major_locator(MaxNLocator(nbins=3, prune="both"))
    inset.yaxis.set_major_locator(MaxNLocator(nbins=3, prune="both"))
    inset_font = max(int(mpl.rcParams.get("font.size", 10)) - 2, 6)
    inset.tick_params(labelsize=inset_font, pad=1)
    if tick_side == "auto":
        tick_side = "right" if "left" in loc else "left"
    if tick_side == "right":
        inset.yaxis.tick_right()
    else:
        inset.yaxis.tick_left()
    if "lower" in loc:
        inset.xaxis.tick_top()
    else:
        inset.xaxis.tick_bottom()
    mark_inset(ax, inset, loc1=connectors[0], loc2=connectors[1], fc="none", ec="0.45", lw=0.6)
    return inset


def safe_legend(
    ax: Any,
    loc: str = "best",
    outside: Literal["right", "top", "bottom"] | None = None,
    ncol: int = 1,
    **kwargs: Any,
) -> Any:
    """Place a readable legend with low risk of covering data."""
    defaults = {
        "frameon": True,
        "framealpha": 0.84,
        "facecolor": "white",
        "edgecolor": "0.82",
        "handlelength": 1.8,
        "columnspacing": 0.9,
        "ncol": ncol,
    }
    defaults.update(kwargs)
    if outside == "right":
        defaults.setdefault("bbox_to_anchor", (1.02, 1.0))
        loc = "upper left"
    elif outside == "top":
        defaults.setdefault("bbox_to_anchor", (0.5, 1.16))
        loc = "lower center"
    elif outside == "bottom":
        defaults.setdefault("bbox_to_anchor", (0.5, -0.22))
        loc = "upper center"
    legend = ax.legend(loc=loc, **defaults)
    legend.set_zorder(20)
    return legend


def save_figure(
    fig: Any,
    stem: str,
    out_dir: str | Path = ".",
    formats: Iterable[str] = ("png",),
    dpi: int = 600,
    pad_inches: float = 0.04,
) -> list[Path]:
    """Save a figure in high-resolution bitmap formats by default."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    if hasattr(fig, "get_constrained_layout") and fig.get_constrained_layout():
        fig.set_constrained_layout_pads(w_pad=0.02, h_pad=0.02, wspace=0.02, hspace=0.02)
    fig.canvas.draw()
    written: list[Path] = []
    for fmt in formats:
        target = out_path / f"{stem}.{fmt.lstrip('.')}"
        fig.savefig(target, dpi=dpi, bbox_inches="tight", pad_inches=pad_inches)
        written.append(target)
    return written
