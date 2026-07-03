"""Country profile generator for Peru (Peru).

Reads the clean LatAm dataset, filters to pais == "Peru" and prints
a Markdown profile section with the 6 required subsections.
"""
import pandas as pd

CSV_PATH = r"C:\Users\carol\capstone-final\data\latam_finanzas_clean.csv"
COUNTRY = "Perú"  # Peru

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
    "gasto_alimentacion_usd": "Alimentacion",
    "gasto_transporte_usd": "Transporte",
    "gasto_entretenimiento_usd": "Entretenimiento",
    "gasto_educacion_usd": "Educacion",
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

    # Housing burden: mean(gasto_vivienda_usd) / mean(ingreso_mensual_usd) * 100
    housing_burden = d["gasto_vivienda_usd"].mean() / ing_mean * 100

    # Spending breakdown: average % of income per gasto column
    # computed as mean(gasto) / mean(ingreso) * 100
    breakdown = {}
    for col in GASTO_COLS:
        breakdown[col] = d[col].mean() / ing_mean * 100

    ahorro_mean = d["ahorro_mensual_usd"].mean()
    pct_neg_savings = (d["ahorro_mensual_usd"] < 0).mean() * 100

    ia_mean = d["horas_herramientas_ia_semana"].mean()
    satis_mean = d["satisfaccion_financiera"].mean()

    lines = []
    lines.append(f"## País: {COUNTRY}")
    lines.append("")
    lines.append("### 1. Muestra y rango de edad")
    lines.append(f"- Tamano de muestra: {n} encuestados")
    lines.append(f"- Rango de edad: {edad_min:.0f} - {edad_max:.0f} anos")
    lines.append("")
    lines.append("### 2. Ingreso mensual (USD)")
    lines.append(f"- Mediana: ${ing_median:,.2f}")
    lines.append(f"- Media: ${ing_mean:,.2f}")
    lines.append(f"- Minimo: ${ing_min:,.2f}")
    lines.append(f"- Maximo: ${ing_max:,.2f}")
    lines.append(f"- Desviacion estandar: ${ing_std:,.2f}")
    lines.append("")
    lines.append("### 3. Carga de vivienda")
    lines.append(
        f"- gasto_vivienda_usd promedio como % del ingreso: {housing_burden:.1f}%"
    )
    lines.append(
        "  (metodo: mean(gasto_vivienda_usd) / mean(ingreso_mensual_usd) * 100)"
    )
    lines.append("")
    lines.append("### 4. Desglose de gasto (% del ingreso)")
    for col in GASTO_COLS:
        lines.append(f"- {GASTO_LABELS[col]}: {breakdown[col]:.1f}%")
    lines.append("")
    lines.append("### 5. Ahorro")
    lines.append(f"- ahorro_mensual_usd promedio: ${ahorro_mean:,.2f}")
    lines.append(f"- % de encuestados con ahorro negativo: {pct_neg_savings:.1f}%")
    lines.append("")
    lines.append("### 6. Herramientas de IA y satisfaccion")
    lines.append(f"- horas_herramientas_ia_semana promedio: {ia_mean:.2f}")
    lines.append(f"- satisfaccion_financiera promedio: {satis_mean:.2f}")

    print("\n".join(lines))

    print(
        f"\nSUMMARY | muestra={n} | ingreso_mediano={ing_median:.2f} | "
        f"carga_vivienda={housing_burden:.1f}%"
    )


if __name__ == "__main__":
    main()
