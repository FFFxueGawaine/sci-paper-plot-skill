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

UNKNOWN_UNIT_MARKERS = {"", "?", "unknown", "unk", "n/a", "na", "none", "null", "未知", "不明", "未定"}
DIMENSIONLESS_UNIT_MARKERS = {
    "-",
    "dimensionless",
    "unitless",
    "non-dimensional",
    "nondimensional",
    "normalized",
    "normalised",
    "无量纲",
    "归一化",
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
    loc: Literal["top-center", "bottom-center"] | None = None,
    ha: Literal["left", "center", "right"] | None = None,
    va: Literal["top", "center", "bottom"] | None = None,
    fontfamily: str | None = None,
) -> None:
    """Place a bold panel label such as '(a)' in a controlled location.

    The default keeps the historical top-center placement. Set ``loc`` for
    the only regular alternative: ``"bottom-center"`` when a journal wants
    panel labels below each axes.
    """
    if size is None:
        import matplotlib as mpl

        size = int(mpl.rcParams.get("font.size", 10)) + 4
    if loc is not None:
        presets = {
            "top-center": (0.5, 1.04, "center", "bottom"),
            "bottom-center": (0.5, -0.20, "center", "top"),
        }
        if loc not in presets:
            raise ValueError("panel_label loc must be 'top-center' or 'bottom-center'.")
        x, y, preset_ha, preset_va = presets[loc]
        if ha is None:
            ha = preset_ha
        if va is None:
            va = preset_va
    if ha is None:
        ha = "center"
    if va is None:
        va = "bottom"
    text_kwargs: dict[str, Any] = {}
    if fontfamily is not None:
        text_kwargs["fontfamily"] = fontfamily
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha=ha,
        va=va,
        fontweight="bold",
        fontsize=size,
        **text_kwargs,
    )


def set_panel_title(
    ax: Any,
    title: str,
    fontfamily: str | None = None,
    lang: Literal["en", "zh"] = "en",
    pad: float = 3.0,
    **kwargs: Any,
) -> Any:
    """Set a panel title with an optional Chinese font.

    Use ``lang="zh"`` or ``fontfamily="SimSun"`` for Chinese manuscript
    figures. English SCI figures should normally keep the global Times New Roman
    style set by ``apply_sci_style``.
    """
    if fontfamily is None and lang == "zh":
        fontfamily = "SimSun"
    if fontfamily is not None:
        kwargs.setdefault("fontfamily", fontfamily)
    kwargs.setdefault("pad", pad)
    return ax.set_title(title, **kwargs)


def format_axis_label(label: str, unit: str | None = None, *, dimensionless: bool = False) -> str:
    """Format an axis label without inventing unknown units.

    Unknown or omitted units return the plain label. Use ``dimensionless=True``
    or an explicit dimensionless marker such as ``"-"`` only when the quantity
    is known to be non-dimensional.
    """
    base = label.strip()
    if not base:
        return base
    if dimensionless:
        return f"{base} (-)"
    if unit is None:
        return base
    unit_text = str(unit).strip()
    bare_unit = unit_text.strip("()").strip()
    normalized = bare_unit.casefold()
    if normalized in UNKNOWN_UNIT_MARKERS:
        return base
    if normalized in DIMENSIONLESS_UNIT_MARKERS:
        return f"{base} (-)"
    return f"{base} ({bare_unit})"


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
    bounds: tuple[float, float, float, float] | None = None,
    borderpad: float = 1.0,
    connectors: tuple[int, int] | None = (2, 4),
    connector_visible: tuple[bool, bool] = (True, True),
    grid: bool = True,
    ypad_fraction: float = 0.08,
    tick_side: Literal["auto", "left", "right"] = "auto",
) -> Any:
    """Create a compact local zoom inset and mark its region on the parent axes.

    Set ``bounds=(x0, y0, w, h)`` in parent-axes coordinates to reserve a
    deterministic blank region for the inset. Use ``connector_visible`` to hide
    any connector line that would cross important data.
    """
    import matplotlib as mpl
    from matplotlib.ticker import MaxNLocator
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

    y0, y1 = ylim
    if ypad_fraction > 0:
        ypad = (y1 - y0) * ypad_fraction
        y0 -= ypad
        y1 += ypad

    if bounds is None:
        inset = inset_axes(ax, width=width, height=height, loc=loc, borderpad=borderpad)
    else:
        inset = inset_axes(
            ax,
            width="100%",
            height="100%",
            loc=loc,
            bbox_to_anchor=bounds,
            bbox_transform=ax.transAxes,
            borderpad=0.0,
        )
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
    if connectors is not None:
        _, connector1, connector2 = mark_inset(
            ax,
            inset,
            loc1=connectors[0],
            loc2=connectors[1],
            fc="none",
            ec="0.45",
            lw=0.6,
        )
        connector1.set_visible(connector_visible[0])
        connector2.set_visible(connector_visible[1])
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


def set_panel_spacing(
    fig: Any,
    w_pad: float = 0.04,
    h_pad: float = 0.04,
    wspace: float = 0.10,
    hspace: float = 0.10,
) -> None:
    """Keep labels, titles, legends, and colorbars from colliding between panels.

    Use this after creating multi-panel figures. Values follow Matplotlib's
    constrained-layout convention: ``w_pad``/``h_pad`` are inches, while
    ``wspace``/``hspace`` are fractions of subplot size.
    """
    if hasattr(fig, "get_constrained_layout") and fig.get_constrained_layout():
        fig.set_constrained_layout_pads(
            w_pad=w_pad,
            h_pad=h_pad,
            wspace=wspace,
            hspace=hspace,
        )
    elif hasattr(fig, "subplots_adjust"):
        fig.subplots_adjust(wspace=wspace, hspace=hspace)
    setattr(fig, "_scimplstyle_layout_applied", True)


def apply_tight_layout(
    fig: Any,
    pad: float = 0.35,
    w_pad: float = 2.0,
    h_pad: float = 1.0,
    rect: tuple[float, float, float, float] | None = None,
) -> None:
    """Apply Matplotlib tight layout after all panel labels and legends exist.

    Use this for dense multi-panel figures when labels should be close but must
    not overlap. Create the figure without ``constrained_layout=True``, add all
    labels/legends/colorbars, then call this function before saving.
    """
    if hasattr(fig, "set_constrained_layout"):
        fig.set_constrained_layout(False)
    kwargs: dict[str, Any] = {"pad": pad, "w_pad": w_pad, "h_pad": h_pad}
    if rect is not None:
        kwargs["rect"] = rect
    fig.tight_layout(**kwargs)
    setattr(fig, "_scimplstyle_layout_applied", True)


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
    if not getattr(fig, "_scimplstyle_layout_applied", False):
        set_panel_spacing(fig)
    fig.canvas.draw()
    written: list[Path] = []
    for fmt in formats:
        target = out_path / f"{stem}.{fmt.lstrip('.')}"
        fig.savefig(target, dpi=dpi, bbox_inches="tight", pad_inches=pad_inches)
        written.append(target)
    return written
