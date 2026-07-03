"""Country profile for Brasil from the clean LatAm finances dataset."""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, "data", "latam_finanzas_clean.csv")
COUNTRY = "Brasil"

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
    edad_min = d["edad"].min()
    edad_max = d["edad"].max()

    ing = d["ingreso_mensual_usd"]
    ing_median = ing.median()
    ing_mean = ing.mean()
    ing_min = ing.min()
    ing_max = ing.max()
    ing_std = ing.std()

    # Housing burden = mean(gasto_vivienda_usd) / mean(ingreso_mensual_usd) * 100
    housing_burden = d["gasto_vivienda_usd"].mean() / ing_mean * 100

    # Spending breakdown: average % of income for each gasto_ column
    # (mean of each expense) / (mean income) * 100
    breakdown = {}
    for c in GASTO_COLS:
        breakdown[c] = d[c].mean() / ing_mean * 100

    ahorro_mean = d["ahorro_mensual_usd"].mean()
    pct_neg = (d["ahorro_mensual_usd"] < 0).mean() * 100

    ia_mean = d["horas_herramientas_ia_semana"].mean()
    satis_mean = d["satisfaccion_financiera"].mean()

    print(f"## País: {COUNTRY}")
    print()
    print(f"### 1. Muestra y rango de edad")
    print(f"- Tamaño de muestra: **{n}** encuestados")
    print(f"- Rango de edad: **{edad_min:.0f} - {edad_max:.0f}** años")
    print()
    print(f"### 2. Ingreso mensual (USD)")
    print(f"- Mediana: **${ing_median:,.2f}**")
    print(f"- Media: **${ing_mean:,.2f}**")
    print(f"- Mínimo: **${ing_min:,.2f}**")
    print(f"- Máximo: **${ing_max:,.2f}**")
    print(f"- Desviación estándar: **${ing_std:,.2f}**")
    print()
    print(f"### 3. Carga de vivienda")
    print(f"- Gasto en vivienda promedio como % del ingreso mensual: **{housing_burden:.1f}%**")
    print(f"  (método: media del gasto_vivienda_usd / media del ingreso_mensual_usd * 100)")
    print()
    print(f"### 4. Desglose de gasto (% del ingreso)")
    for c in GASTO_COLS:
        print(f"- {GASTO_LABELS[c]}: **{breakdown[c]:.1f}%**")
    print()
    print(f"### 5. Ahorro")
    print(f"- Ahorro mensual promedio: **${ahorro_mean:,.2f}**")
    print(f"- Encuestados con ahorro negativo: **{pct_neg:.1f}%**")
    print()
    print(f"### 6. Herramientas de IA y satisfacción")
    print(f"- Horas promedio con herramientas de IA por semana: **{ia_mean:.2f}**")
    print(f"- Satisfacción financiera promedio: **{satis_mean:.2f}**")
    print()
    print(f"SUMMARY | muestra={n} | ingreso_mediano={ing_median:.2f} | carga_vivienda={housing_burden:.1f}%")


if __name__ == "__main__":
    main()
