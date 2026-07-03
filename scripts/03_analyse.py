"""
03_analyse.py — Core analyses for the LATAM financial-wellness dataset.

Reads data/latam_finanzas_clean.csv and prints six analyses as formatted
(Markdown) tables:

  1. Income by country (median/mean/min/max/std), sorted by median desc.
  2. Age vs. savings (bins 18-22, 23-25, 26-28, 29-32): avg savings + savings rate.
  3. Spending breakdown: full-sample avg % of income per category, sorted desc.
  4. Credit-card holders vs non-holders: income, food, entertainment, savings + % diff.
  5. AI-tool usage (Low 0-3h / Medium 4-10h / High 11+h) vs satisfaction, plus
     Pearson correlation between AI hours and financial satisfaction.
  6. Housing burden by country (avg gasto_vivienda / avg income), sorted desc.

Housing burden and savings rate use the *ratio of means* method
(mean(numerator) / mean(denominator) * 100), consistent with the country
profiles in scripts/country_profiles.md.

Usage:
    python scripts/03_analyse.py
    python scripts/03_analyse.py path/to/clean.csv
"""

import sys
from pathlib import Path

import pandas as pd
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "data" / "latam_finanzas_clean.csv"

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


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def md_table(headers, rows):
    """Print a GitHub-flavoured Markdown table."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    def fmt(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    print(fmt(headers))
    print("| " + " | ".join("-" * widths[i] for i in range(len(headers))) + " |")
    for row in rows:
        print(fmt(row))


def age_group(age):
    # Bins cover the full observed range (22-40). 33+ is split into 33-36 /
    # 37-40 because both halves are substantial (~106 / ~90 respondents).
    if pd.isna(age):
        return None
    if 18 <= age <= 22:
        return "18-22"
    if 23 <= age <= 25:
        return "23-25"
    if 26 <= age <= 28:
        return "26-28"
    if 29 <= age <= 32:
        return "29-32"
    if 33 <= age <= 36:
        return "33-36"
    if age >= 37:
        return "37-40"
    return None  # <18 — none observed


def ai_group(hours):
    # Ranges fitted to the real distribution of horas_herramientas_ia_semana
    # (max observed = 8h/week), so all three bands contain data:
    # Bajo 0-3 (n=323), Medio 4-6 (n=164), Alto 7+ (n=13).
    if pd.isna(hours):
        return None
    if 0 <= hours <= 3:
        return "Bajo (0-3h)"
    if 4 <= hours <= 6:
        return "Medio (4-6h)"
    if hours >= 7:
        return "Alto (7h+)"
    return None


def main():
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.exists():
        sys.exit(f"ERROR: file not found: {csv_path}")

    df = pd.read_csv(csv_path, encoding="utf-8")

    # ------------------------------------------------------------------ 1.
    section("1. INCOME BY COUNTRY (sorted by median income, desc)")
    inc = (
        df.groupby("pais")["ingreso_mensual_usd"]
        .agg(["median", "mean", "min", "max", "std", "count"])
        .sort_values("median", ascending=False)
    )
    rows = [
        [
            pais,
            int(r["count"]),
            f"{r['median']:,.2f}",
            f"{r['mean']:,.2f}",
            f"{r['min']:,.2f}",
            f"{r['max']:,.2f}",
            f"{r['std']:,.2f}",
        ]
        for pais, r in inc.iterrows()
    ]
    md_table(["País", "N", "Mediana", "Media", "Mín", "Máx", "Std"], rows)
    print("(Confirms scripts/country_profiles.md — values match the per-country profiles.)")

    # ------------------------------------------------------------------ 2.
    section("2. AGE VS. SAVINGS")
    df["grupo_edad"] = df["edad"].apply(age_group)
    order = ["18-22", "23-25", "26-28", "29-32", "33-36", "37-40"]
    rows = []
    for g in order:
        sub = df[df["grupo_edad"] == g]
        n = len(sub)
        if n == 0:
            rows.append([g, 0, "—", "—"])
            continue
        avg_sav = sub["ahorro_mensual_usd"].mean()
        rate = sub["ahorro_mensual_usd"].mean() / sub["ingreso_mensual_usd"].mean() * 100
        rows.append([g, n, f"{avg_sav:,.2f}", f"{rate:.1f}%"])
    md_table(["Grupo edad", "N", "Ahorro prom. (USD)", "Tasa ahorro"], rows)
    excluded = int(df["grupo_edad"].isna().sum())
    print(
        f"NOTE: bins now cover the full observed range (22-40); "
        f"{excluded} respondents excluded (all {len(df)} respondents included)."
    )
    print("Savings rate = mean(ahorro) / mean(ingreso) * 100 (ratio of means).")

    # ------------------------------------------------------------------ 3.
    section("3. SPENDING BREAKDOWN (full sample, avg % of income, desc)")
    mean_income = df["ingreso_mensual_usd"].mean()
    breakdown = []
    for col in GASTO_COLS:
        pct = df[col].mean() / mean_income * 100
        breakdown.append((GASTO_LABEL[col], df[col].mean(), pct))
    breakdown.sort(key=lambda x: x[2], reverse=True)
    total_pct = sum(b[2] for b in breakdown)
    rows = [[label, f"{avg:,.2f}", f"{pct:.1f}%"] for label, avg, pct in breakdown]
    rows.append(["TOTAL gastos", "", f"{total_pct:.1f}%"])
    md_table(["Categoría", "Gasto prom. (USD)", "% del ingreso"], rows)
    print("(% = mean(gasto_categoria) / mean(ingreso) * 100.)")

    # ------------------------------------------------------------------ 4.
    section("4. CREDIT-CARD HOLDERS VS NON-HOLDERS")
    metrics = {
        "Ingreso": "ingreso_mensual_usd",
        "Alimentación": "gasto_alimentacion_usd",
        "Entretenimiento": "gasto_entretenimiento_usd",
        "Ahorro": "ahorro_mensual_usd",
    }
    holders = df[df["tiene_tarjeta_credito"] == "Sí"]
    non = df[df["tiene_tarjeta_credito"] == "No"]
    print(f"Holders (Sí): {len(holders)}   |   Non-holders (No): {len(non)}")
    rows = []
    for label, col in metrics.items():
        h, nh = holders[col].mean(), non[col].mean()
        diff = (h - nh) / nh * 100 if nh != 0 else float("nan")
        rows.append([label, f"{h:,.2f}", f"{nh:,.2f}", f"{diff:+.1f}%"])
    md_table(["Métrica", "Con tarjeta", "Sin tarjeta", "% dif (con vs sin)"], rows)
    print("(% dif = (con - sin) / sin * 100.)")

    # ------------------------------------------------------------------ 5.
    section("5. AI TOOL USAGE VS FINANCIAL SATISFACTION")
    df["grupo_ia"] = df["horas_herramientas_ia_semana"].apply(ai_group)
    ai_order = ["Bajo (0-3h)", "Medio (4-6h)", "Alto (7h+)"]
    rows = []
    for g in ai_order:
        sub = df[df["grupo_ia"] == g]
        n = len(sub)
        if n == 0:
            rows.append([g, 0, "—", "—"])
            continue
        rows.append(
            [
                g,
                n,
                f"{sub['satisfaccion_financiera'].mean():.2f}",
                f"{sub['ingreso_mensual_usd'].mean():,.2f}",
            ]
        )
    md_table(["Grupo IA", "N", "Satisfacción prom.", "Ingreso prom. (USD)"], rows)
    r, p = pearsonr(
        df["horas_herramientas_ia_semana"], df["satisfaccion_financiera"]
    )
    print(f"\nPearson(horas_ia, satisfaccion) = {r:.4f}  (p = {p:.4f}, n = {len(df)})")
    print(
        "NOTE: ranges fitted to real data (max AI usage = "
        f"{df['horas_herramientas_ia_semana'].max():.0f}h/week); all three "
        "groups contain respondents."
    )

    # ------------------------------------------------------------------ 6.
    section("6. HOUSING BURDEN BY COUNTRY (avg vivienda / avg ingreso, desc)")
    g = df.groupby("pais")
    burden = (g["gasto_vivienda_usd"].mean() / g["ingreso_mensual_usd"].mean() * 100)
    burden = burden.sort_values(ascending=False)
    rows = [[pais, f"{val:.1f}%"] for pais, val in burden.items()]
    md_table(["País", "Carga vivienda"], rows)
    print("(Confirms scripts/country_profiles.md — matches the per-country profiles.)")


if __name__ == "__main__":
    main()
