"""Country profile generator for Colombia.

Reads the clean LatAm dataset, filters to Colombia, and prints a Markdown
profile section with sample size, income stats, housing burden, spending
breakdown, savings, and AI-tool usage.
"""

import os
import pandas as pd

COUNTRY = "Colombia"

# Resolve the clean CSV relative to the project root (parent of scripts/).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "latam_finanzas_clean.csv")

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
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    d = df[df["pais"] == COUNTRY].copy()

    n = len(d)
    edad_min = d["edad"].min()
    edad_max = d["edad"].max()

    ing = d["ingreso_mensual_usd"]
    ing_median = ing.median()
    ing_mean = ing.mean()
    ing_min = ing.min()
    ing_max = ing.max()
    ing_std = ing.std()

    # Housing burden: mean(gasto_vivienda) / mean(ingreso) * 100 (aggregate method).
    housing_burden = d["gasto_vivienda_usd"].mean() / ing_mean * 100

    # Spending breakdown: mean(gasto_x) / mean(ingreso) * 100 for each column.
    breakdown = {
        col: d[col].mean() / ing_mean * 100 for col in GASTO_COLS
    }

    ahorro_mean = d["ahorro_mensual_usd"].mean()
    pct_ahorro_negativo = (d["ahorro_mensual_usd"] < 0).mean() * 100

    ia_mean = d["horas_herramientas_ia_semana"].mean()
    satis_mean = d["satisfaccion_financiera"].mean()

    print(f"## País: {COUNTRY}")
    print()
    print("### 1. Muestra y rango de edad")
    print(f"- Tamaño de muestra: {n} encuestados")
    print(f"- Rango de edad: {edad_min:.0f} a {edad_max:.0f} años")
    print()
    print("### 2. Ingreso mensual (USD)")
    print(f"- Mediana: ${ing_median:,.2f}")
    print(f"- Media: ${ing_mean:,.2f}")
    print(f"- Mínimo: ${ing_min:,.2f}")
    print(f"- Máximo: ${ing_max:,.2f}")
    print(f"- Desviación estándar: ${ing_std:,.2f}")
    print()
    print("### 3. Carga de vivienda")
    print(f"- gasto_vivienda_usd promedio como % del ingreso: {housing_burden:.1f}%")
    print("  (método agregado: mean(gasto_vivienda_usd) / mean(ingreso_mensual_usd) * 100)")
    print()
    print("### 4. Desglose de gasto (% del ingreso, método agregado)")
    for col in GASTO_COLS:
        print(f"- {GASTO_LABELS[col]}: {breakdown[col]:.1f}%")
    print()
    print("### 5. Ahorro")
    print(f"- ahorro_mensual_usd promedio: ${ahorro_mean:,.2f}")
    print(f"- % de encuestados con ahorro negativo: {pct_ahorro_negativo:.1f}%")
    print()
    print("### 6. Herramientas de IA y satisfacción")
    print(f"- horas_herramientas_ia_semana promedio: {ia_mean:.2f}")
    print(f"- satisfaccion_financiera promedio: {satis_mean:.2f}")
    print()
    print(
        f"SUMMARY | muestra={n} | "
        f"ingreso_mediano={ing_median:.2f} | "
        f"carga_vivienda={housing_burden:.1f}%"
    )


if __name__ == "__main__":
    main()
