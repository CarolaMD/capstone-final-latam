"""
04_visualise.py — Generate the 5 report charts for the LATAM finance dataset.

Reads data/latam_finanzas_clean.csv and writes 5 PNGs to charts/:
  01_income_by_country.png       horizontal box plot, sorted by median income
  02_age_vs_savings.png          scatter (age vs savings) + regression, by country
  03_spending_breakdown.png      horizontal bars, avg % of income per category
  04_satisfaction_by_ai_usage.png bars, avg satisfaction by AI-usage group
  05_housing_burden_by_country.png horizontal bars, housing % of income, red→green

Palette: validated reference categorical + status ramp from the dataviz skill
(colorblind-checked; worst adjacent CVD ΔE 24.2). Not matplotlib defaults.

NOTE: satisfaccion_financiera is a 1-10 scale in this dataset (means ~6), so
chart 04 uses a 1-10 y-axis, not 1-5.

Usage:
    python scripts/04_visualise.py
    python scripts/04_visualise.py path/to/clean.csv
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "data" / "latam_finanzas_clean.csv"
CHART_DIR = ROOT / "charts"

SOURCE_NOTE = (
    "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"
)

# ---- Validated palette (from dataviz skill reference, light mode) ----------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"        # primary
INK_2 = "#52514e"      # secondary
MUTED = "#898781"      # axis/labels
GRID = "#e1e0d9"       # hairline gridline
BASELINE = "#c3c2b7"

# Categorical slots in fixed CVD-safe order (blue, aqua, yellow, green, violet, red)
CATEGORICAL = ["#2a78d6", "#1baf7a", "#eda100", "#008300", "#4a3aa7", "#e34948"]
PRIMARY_BLUE = "#2a78d6"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]
GASTO_LABEL = {
    "gasto_vivienda_usd": "Vivienda",
    "gasto_alimentacion_usd": "Alimentación",
    "gasto_transporte_usd": "Transporte",
    "gasto_entretenimiento_usd": "Entretenimiento",
    "gasto_educacion_usd": "Educación",
    "gasto_salud_usd": "Salud",
}


def apply_style():
    plt.rcParams.update(
        {
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "text.color": INK,
            "axes.edgecolor": BASELINE,
            "axes.labelcolor": INK_2,
            "axes.titlecolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
        }
    )


def finish(fig, ax, path):
    """Common chrome: recessive spines, source note, tight save."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BASELINE)
    fig.text(
        0.01, 0.01, SOURCE_NOTE, fontsize=8, color=MUTED, ha="left", va="bottom"
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  saved {path.relative_to(ROOT)}")


def ai_group(h):
    if pd.isna(h):
        return None
    if 0 <= h <= 3:
        return "Bajo (0-3h)"
    if 4 <= h <= 6:
        return "Medio (4-6h)"
    if h >= 7:
        return "Alto (7h+)"
    return None


# ---------------------------------------------------------------- charts ----
def chart1_income(df):
    order = (
        df.groupby("pais")["ingreso_mensual_usd"].median().sort_values().index.tolist()
    )  # ascending → highest ends on top in a horizontal boxplot
    data = [df.loc[df["pais"] == c, "ingreso_mensual_usd"].values for c in order]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bp = ax.boxplot(
        data, orientation="horizontal", patch_artist=True, widths=0.6,
        medianprops=dict(color=INK, linewidth=2),
        whiskerprops=dict(color=BASELINE), capprops=dict(color=BASELINE),
        flierprops=dict(marker="o", markersize=4, markerfacecolor=MUTED,
                        markeredgecolor="none", alpha=0.5),
    )
    for box in bp["boxes"]:
        box.set(facecolor=PRIMARY_BLUE, edgecolor=SURFACE, linewidth=1.5, alpha=0.9)
    ax.set_yticklabels(order)
    ax.set_xlabel("Ingreso mensual (USD)")
    ax.set_ylabel("País")
    ax.set_title("Distribución del ingreso mensual por país",
                 fontsize=14, fontweight="bold", pad=12)
    ax.grid(axis="y", visible=False)
    finish(fig, ax, CHART_DIR / "01_income_by_country.png")


def chart2_age_savings(df):
    fig, ax = plt.subplots(figsize=(9, 6))
    countries = sorted(df["pais"].unique())
    for i, c in enumerate(countries):
        sub = df[df["pais"] == c]
        ax.scatter(sub["edad"], sub["ahorro_mensual_usd"],
                   s=32, color=CATEGORICAL[i % len(CATEGORICAL)],
                   edgecolor=SURFACE, linewidth=0.6, alpha=0.85, label=c)
    # overall linear regression trend line
    x, y = df["edad"].values, df["ahorro_mensual_usd"].values
    slope, intercept = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, slope * xs + intercept, color=INK, linewidth=2, linestyle="--",
            label=f"Tendencia (pend. {slope:.1f} USD/año)")
    ax.set_xlabel("Edad (años)")
    ax.set_ylabel("Ahorro mensual (USD)")
    ax.set_title("Edad vs. ahorro mensual, por país",
                 fontsize=14, fontweight="bold", pad=12)
    ax.legend(frameon=False, fontsize=9, loc="upper right", ncol=2)
    finish(fig, ax, CHART_DIR / "02_age_vs_savings.png")


def chart3_spending(df):
    mean_income = df["ingreso_mensual_usd"].mean()
    items = [(GASTO_LABEL[c], df[c].mean() / mean_income * 100) for c in GASTO_COLS]
    items.sort(key=lambda t: t[1])  # ascending → highest on top
    labels = [t[0] for t in items]
    values = [t[1] for t in items]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(labels, values, color=PRIMARY_BLUE, edgecolor=SURFACE,
                   linewidth=1.5, height=0.68)
    for b, v in zip(bars, values):
        ax.text(v + 0.4, b.get_y() + b.get_height() / 2, f"{v:.1f}%",
                va="center", ha="left", color=INK_2, fontsize=10)
    ax.set_xlabel("% del ingreso mensual promedio")
    ax.set_ylabel("Categoría de gasto")
    ax.set_title("Desglose del gasto: % del ingreso por categoría",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlim(0, max(values) * 1.15)
    ax.grid(axis="y", visible=False)
    finish(fig, ax, CHART_DIR / "03_spending_breakdown.png")


def chart4_satisfaction_ai(df):
    df = df.copy()
    df["grupo_ia"] = df["horas_herramientas_ia_semana"].apply(ai_group)
    order = ["Bajo (0-3h)", "Medio (4-6h)", "Alto (7h+)"]
    means = [df.loc[df["grupo_ia"] == g, "satisfaccion_financiera"].mean() for g in order]
    ns = [int((df["grupo_ia"] == g).sum()) for g in order]
    fig, ax = plt.subplots(figsize=(8, 5.5))
    bars = ax.bar(order, means, color=PRIMARY_BLUE, edgecolor=SURFACE,
                  linewidth=1.5, width=0.6)
    for b, v, n in zip(bars, means, ns):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.15, f"{v:.2f}",
                ha="center", va="bottom", color=INK, fontsize=12, fontweight="bold")
        ax.text(b.get_x() + b.get_width() / 2, 0.2, f"n={n}",
                ha="center", va="bottom", color=SURFACE, fontsize=9)
    ax.set_ylim(0, 10)
    ax.set_ylabel("Satisfacción financiera promedio (escala 1–10)")
    ax.set_xlabel("Uso de herramientas de IA (horas/semana)")
    ax.set_title("Satisfacción financiera según uso de herramientas de IA",
                 fontsize=14, fontweight="bold", pad=12)
    ax.grid(axis="x", visible=False)
    finish(fig, ax, CHART_DIR / "04_satisfaction_by_ai_usage.png")


def chart5_housing(df):
    g = df.groupby("pais")
    burden = (g["gasto_vivienda_usd"].mean() / g["ingreso_mensual_usd"].mean() * 100)
    burden = burden.sort_values()  # ascending → highest on top
    labels = burden.index.tolist()
    values = burden.values
    # red→green gradient: high burden = red (bad), low burden = green (good)
    cmap = LinearSegmentedColormap.from_list("burden", ["#0ca30c", "#fab219", "#d03b3b"])
    norm = (values - values.min()) / (values.max() - values.min())
    colors = [cmap(n) for n in norm]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(labels, values, color=colors, edgecolor=SURFACE,
                   linewidth=1.5, height=0.68)
    for b, v in zip(bars, values):
        ax.text(v + 0.25, b.get_y() + b.get_height() / 2, f"{v:.1f}%",
                va="center", ha="left", color=INK_2, fontsize=10)
    ax.axvline(30, color=MUTED, linestyle=":", linewidth=1.2)
    ax.text(30, len(labels) - 0.4, " umbral 30%", color=MUTED, fontsize=8, va="top")
    ax.set_xlabel("Gasto en vivienda como % del ingreso")
    ax.set_ylabel("País")
    ax.set_title("Carga de vivienda por país (rojo = mayor carga)",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlim(0, max(values) * 1.15)
    ax.grid(axis="y", visible=False)
    finish(fig, ax, CHART_DIR / "05_housing_burden_by_country.png")


def main():
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.exists():
        sys.exit(f"ERROR: file not found: {csv_path}")
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path, encoding="utf-8")
    apply_style()
    print("Generating charts:")
    chart1_income(df)
    chart2_age_savings(df)
    chart3_spending(df)
    chart4_satisfaction_ai(df)
    chart5_housing(df)
    print("Done.")


if __name__ == "__main__":
    main()
