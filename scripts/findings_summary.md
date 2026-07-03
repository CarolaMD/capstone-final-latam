# Resumen de Hallazgos — Análisis LatAm 2025

Fuente: `data/latam_finanzas_clean.csv` (500 encuestados, jóvenes profesionales
de 6 países de América Latina). Generado por `scripts/03_analyse.py`.

Notas de método:
- Carga de vivienda y tasa de ahorro se calculan como *razón de promedios*:
  `mean(numerador) / mean(denominador) * 100`.
- El ingreso, ahorro, edad, satisfacción y horas de IA tuvieron imputación por
  mediana en la Fase 2 (ver `scripts/02_clean.py`). Por eso varios países comparten
  la mediana global de ingreso de $1,784.81.

---

## 1. Ingreso por país

Ingreso mediano mensual (USD), de mayor a menor:
Colombia: $1,840.79 — Argentina: $1,788.17 — Brasil: $1,784.81 — Chile: $1,784.81 — Perú: $1,784.81 — México: $1,758.35

Detalle completo por país — media / mínimo / máximo / desviación estándar (USD):
Colombia: 1,862.66 / 300.00 / 3,290.47 / 673.12 — Argentina: 1,723.22 / 300.00 / 3,833.55 / 735.18 — Brasil: 1,729.84 / 300.00 / 2,927.78 / 583.55 — Chile: 1,811.58 / 300.00 / 3,009.15 / 600.53 — Perú: 1,775.94 / 300.00 / 3,494.29 / 688.81 — México: 1,753.17 / 300.00 / 3,618.37 / 810.85

Tamaño de muestra por país:
Perú: 94 — Brasil: 92 — Colombia: 85 — Argentina: 78 — México: 78 — Chile: 73 (total: 500)

Nota: el empate de mediana en $1,784.81 (Brasil, Chile, Perú) es un artefacto de la
imputación con la mediana global del ingreso en la Fase 2, no un error de cálculo.

---

## 2. Edad vs. ahorro

Grupos que cubren toda la muestra (edades observadas: 22-40). Cada grupo:
ahorro mensual promedio (USD) y tasa de ahorro (ahorro/ingreso %):
18-22: $285.40 (14.9%) — 23-25: $266.65 (15.1%) — 26-28: $246.92 (14.8%) — 29-32: $236.36 (13.2%) — 33-36: $253.00 (14.0%) — 37-40: $236.15 (13.2%)

Tamaño de cada grupo:
18-22: 21 — 23-25: 81 — 26-28: 73 — 29-32: 129 — 33-36: 106 — 37-40: 90 (total: 500)

Patrón: los más jóvenes (18-25) ahorran más en monto y tasa (~15%); los grupos
mayores bajan hacia ~13%, con un ligero repunte en 33-36.

---

## 3. Desglose de gasto (muestra completa)

Gasto promedio como % del ingreso, de mayor a menor:
Vivienda: 30.3% — Alimentación: 15.3% — Transporte: 8.1% — Entretenimiento: 6.0% — Educación: 5.1% — Salud: 4.9%

Total de gastos categorizados: 69.6% del ingreso.

Gasto promedio en USD por categoría:
Vivienda: $538.84 — Alimentación: $270.82 — Transporte: $143.33 — Entretenimiento: $106.28 — Educación: $90.27 — Salud: $87.11

---

## 4. Tenedores de tarjeta de crédito vs. no tenedores

Tamaños: con tarjeta (Sí): 255 — sin tarjeta (No): 245

Cada métrica — promedio con tarjeta / promedio sin tarjeta / % diferencia (con vs. sin):
Ingreso: $1,733.43 / $1,819.55 / -4.7% — Alimentación: $264.68 / $277.22 / -4.5% — Entretenimiento: $107.10 / $105.43 / +1.6% — Ahorro: $264.68 / $231.37 / +14.4%

Hallazgo destacado: los tenedores de tarjeta ganan un poco menos (-4.7%) pero
ahorran 14.4% más. (Los dos valores de $264.68 son coincidencia entre columnas
distintas: alimentación de tenedores y ahorro de tenedores.)

---

## 5. Uso de herramientas de IA vs. satisfacción financiera

Rangos ajustados a la distribución real (máximo observado: 8 h/semana). Cada grupo:
N — satisfacción promedio (escala 1-10) — ingreso promedio (USD):
Bajo (0-3h): 323 — 6.24 — $1,765.21 — Medio (4-6h): 164 — 6.00 — $1,791.88 — Alto (7h+): 13 — 6.23 — $1,829.45

Correlación de Pearson entre horas_herramientas_ia_semana y satisfaccion_financiera:
r = -0.058 — p = 0.196 — n = 500

Interpretación: no hay correlación estadísticamente significativa (p > 0.05). La
satisfacción es prácticamente plana entre grupos (6.00-6.24). El ingreso sí sube de
forma monótona con el uso de IA (+$64 de Bajo a Alto), pero el grupo Alto es pequeño
(n=13), así que conviene no sobreinterpretar.

---

## 6. Carga de vivienda por país

Gasto promedio en vivienda como % del ingreso promedio, de mayor a menor:
Argentina: 31.8% — Colombia: 31.3% — México: 31.2% — Chile: 29.8% — Perú: 29.6% — Brasil: 28.6%
