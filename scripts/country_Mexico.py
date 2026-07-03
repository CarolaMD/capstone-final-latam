"""Country profile for Mexico from the clean LatAm dataset.

Reads data/latam_finanzas_clean.csv (UTF-8), filters to pais == "Mexico",
and prints a Markdown profile section.
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, "data", "latam_finanzas_clean.csv")

COUNTRY = "México"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]

GASTO_LABELS = {
    "gasto_vivienda_usd": "Vivienda",
    "gasto_alimentacion_usd": "Alimentación",
    "gasto_transporte_usd": "Transporte",
    "gasto_entretenimiento_usd": "Entretenimiento",
    "gasto_educacion_usd": "Educación",
    "gasto_salud_usd": "Salud",
}


def main():
    df = pd.read_csv(CSV, encoding="utf-8")
    d = df[df["pais"] == COUNTRY].copy()

    n = len(d)

    # 1. Sample + age range
    edad_min = d["edad"].min()
    edad_max = d["edad"].max()

    # 2. Income stats
    ing = d["ingreso_mensual_usd"]
    ing_median = ing.median()
    ing_mean = ing.mean()
    ing_min = ing.min()
    ing_max = ing.max()
    ing_std = ing.std()

    # 3. Housing burden (aggregate mean-of-column approach)
    carga = d["gasto_vivienda_usd"].mean() / ing_mean * 100

    # 4. Spending breakdown: mean of (per-respondent gasto / ingreso) * 100
    # Use aggregate mean-of-column / mean income for consistency.
    breakdown = {}
    for c in GASTO_COLS:
        breakdown[c] = d[c].mean() / ing_mean * 100

    # 5. Savings
    ahorro_mean = d["ahorro_mensual_usd"].mean()
    pct_neg = (d["ahorro_mensual_usd"] < 0).mean() * 100

    # 6. AI tools + satisfaction
    ia_mean = d["horas_herramientas_ia_semana"].mean()
    sat_mean = d["satisfaccion_financiera"].mean()

    lines = []
    lines.append(f"## País: {COUNTRY}")
    lines.append("")
    lines.append(f"### 1. Muestra y rango de edad")
    lines.append(f"- Tamaño de muestra: {n} encuestados")
    lines.append(f"- Rango de edad: {edad_min:.0f} - {edad_max:.0f} años")
    lines.append("")
    lines.append(f"### 2. Ingreso mensual (USD)")
    lines.append(f"- Mediana: ${ing_median:,.2f}")
    lines.append(f"- Media: ${ing_mean:,.2f}")
    lines.append(f"- Mínimo: ${ing_min:,.2f}")
    lines.append(f"- Máximo: ${ing_max:,.2f}")
    lines.append(f"- Desviación estándar: ${ing_std:,.2f}")
    lines.append("")
    lines.append(f"### 3. Carga de vivienda")
    lines.append(
        f"- Gasto promedio en vivienda como % del ingreso mensual promedio: {carga:.1f}%"
    )
    lines.append("  (método: media de columna gasto_vivienda_usd / media de ingreso_mensual_usd)")
    lines.append("")
    lines.append(f"### 4. Desglose de gastos (% del ingreso mensual promedio)")
    for c in GASTO_COLS:
        lines.append(f"- {GASTO_LABELS[c]}: {breakdown[c]:.1f}%")
    lines.append("")
    lines.append(f"### 5. Ahorro")
    lines.append(f"- Ahorro mensual promedio: ${ahorro_mean:,.2f}")
    lines.append(f"- % de encuestados con ahorro negativo: {pct_neg:.1f}%")
    lines.append("")
    lines.append(f"### 6. Herramientas de IA y satisfacción")
    lines.append(f"- Horas promedio de herramientas de IA por semana: {ia_mean:.2f}")
    lines.append(f"- Satisfacción financiera promedio: {sat_mean:.2f}")
    lines.append("")

    print("\n".join(lines))

    print(
        f"SUMMARY | muestra={n} | ingreso_mediano={ing_median:.2f} | "
        f"carga_vivienda={carga:.1f}%"
    )


if __name__ == "__main__":
    main()
