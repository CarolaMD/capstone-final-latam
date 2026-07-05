# Data Quality Log — Questions and Answers

## 1. What problem did you find in the `industria` column?

29 spelling variants were found for the same categories: differences in
capitalization, accents, abbreviations, and synonyms (for example "TEC", "ti",
"Tech", "Tecnología" all referring to the same industry). These variants were
standardized into 7 canonical categories using a normalization map.

## 2. What did you decide to do about missing values in `gasto_salud_usd`?

Missing values were imputed with the **median** of the column, following the
same approach applied to the other numeric columns with up to 40% missing
values (age, income, savings, financial satisfaction, and weekly AI tool usage
hours). This preserved all 500 records without dropping any rows. The
exception was `deuda_total_usd`, with 45% missing values, which was left
unimputed because that percentage was too high to fill in reliably.

## 3. How many respondents have negative savings?

110 records show negative monthly savings (spending that exceeds income).
These are valid data points and were not removed; they were flagged with the
boolean column `ahorro_negativo` for use in financial risk analysis.

---

*Source: `analysis-report.md`, Section 2 (Methodology) — synthetic data, see
the notice at the beginning of the report.*
