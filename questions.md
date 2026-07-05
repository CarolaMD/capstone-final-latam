# Data Quality Log — Preguntas y Respuestas

## 1. ¿Qué problema encontraste en la columna `industria`?

Se encontraron 29 variantes de escritura para las mismas categorías: diferencias de
mayúsculas/minúsculas, acentos, abreviaturas y sinónimos (por ejemplo "TEC", "ti",
"Tech", "Tecnología" refiriéndose todos a la misma industria). Estas variantes se
estandarizaron a 7 categorías canónicas mediante un mapa de normalización.

## 2. ¿Qué decidiste hacer con los valores faltantes de `gasto_salud_usd`?

Se imputó con la **mediana** de la columna, siguiendo el mismo criterio aplicado a
las demás columnas numéricas con hasta 40% de valores ausentes (edad, ingreso,
ahorro, satisfacción financiera y horas de uso de IA). Esto permitió conservar los
500 registros sin descartar filas. La excepción fue `deuda_total_usd`, con 45% de
valores faltantes, que se dejó sin imputar por ser un porcentaje demasiado alto
para hacerlo de forma confiable.

## 3. ¿Cuántos encuestados tienen ahorro negativo?

110 registros presentan ahorro mensual negativo (gasto que excede el ingreso). Son
datos válidos y no se eliminaron; se marcaron con la columna booleana
`ahorro_negativo` para su uso en análisis de riesgo financiero.

---

*Fuente: `analysis-report.md`, sección 2 (Metodología) — datos sintéticos, ver
aviso al inicio del reporte.*
