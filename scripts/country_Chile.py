"""Country profile for Chile from the clean LatAm finances dataset."""
import os
import pandas as pd

COUNTRY = "Chile"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, "data", "latam_finanzas_clean.csv")

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
    d = df[df["pais"] == COUNTRY]

    n = len(d)
    edad_min, edad_max = d["edad"].min(), d["edad"].max()

    ing = d["ingreso_mensual_usd"]
    ing_median = ing.median()
    ing_mean = ing.mean()
    ing_min = ing.min()
    ing_max = ing.max()
    ing_std = ing.std()

    mean_ing = ing.mean()
    # Housing burden: mean(gasto_vivienda_usd) / mean(ingreso_mensual_usd) * 100
    carga_vivienda = d["gasto_vivienda_usd"].mean() / mean_ing * 100

    # Spending breakdown: mean(gasto)/mean(ingreso)*100 per category
    breakdown = {
        c: d[c].mean() / mean_ing * 100 for c in GASTO_COLS
    }

    ahorro_mean = d["ahorro_mensual_usd"].mean()
    pct_neg = (d["ahorro_mensual_usd"] < 0).mean() * 100

    ia_mean = d["horas_herramientas_ia_semana"].mean()
    satis_mean = d["satisfaccion_financiera"].mean()

    print(f"## País: {COUNTRY}\n")

    print("### 1. Muestra y rango de edad")
    print(f"- Tamaño de muestra: **{n}** encuestados")
    print(f"- Rango de edad: **{edad_min:.0f} - {edad_max:.0f}** años\n")

    print("### 2. Ingreso mensual (USD)")
    print(f"- Mediana: **${ing_median:,.2f}**")
    print(f"- Media: **${ing_mean:,.2f}**")
    print(f"- Mínimo: **${ing_min:,.2f}**")
    print(f"- Máximo: **${ing_max:,.2f}**")
    print(f"- Desviación estándar: **${ing_std:,.2f}**\n")

    print("### 3. Carga de vivienda")
    print(f"- Gasto promedio en vivienda como % del ingreso: **{carga_vivienda:.1f}%**")
    print(f"- Método: mean(gasto_vivienda_usd) / mean(ingreso_mensual_usd) * 100\n")

    print("### 4. Desglose de gastos (% promedio del ingreso)")
    for c in GASTO_COLS:
        print(f"- {GASTO_LABELS[c]}: **{breakdown[c]:.1f}%**")
    print()

    print("### 5. Ahorro")
    print(f"- Ahorro mensual promedio: **${ahorro_mean:,.2f}**")
    print(f"- Encuestados con ahorro negativo: **{pct_neg:.1f}%**\n")

    print("### 6. Herramientas de IA y satisfacción financiera")
    print(f"- Horas promedio de herramientas de IA por semana: **{ia_mean:.2f}**")
    print(f"- Satisfacción financiera promedio: **{satis_mean:.2f}**\n")

    print(f"SUMMARY | muestra={n} | ingreso_mediano={ing_median:.2f} | "
          f"carga_vivienda={carga_vivienda:.1f}%")


if __name__ == "__main__":
    main()
