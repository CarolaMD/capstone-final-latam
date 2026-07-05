# Pipeline: Análisis LatAm 2025

## Project
Repeatable financial wellness analysis pipeline for Futuro Digital LatAm.
Dataset: data/latam_finanzas_2025.csv (raw) → data/latam_finanzas_clean.csv (clean)
Report: analysis-report.md

## Python Environment
venv activated. Libraries: pandas, matplotlib, seaborn, scipy.
Scripts go in scripts/. Charts go in charts/ as PNGs.

## Naming Conventions
Scripts: 01_explore.py, 02_clean.py, 03_analyse.py, 04_visualise.py
Charts: 01_income_by_country.png through 05_housing_burden_by_country.png
Country scripts: country_Mexico.py, country_Colombia.py, etc.

## Notion Workspace
Integration: LatAm Pipeline
Databases: "Findings Tracker", "Country Profiles"
Report page: "Informe Ejecutivo"
Push each finding after Phase 3 analysis. Push report after Phase 6.

## Pipeline Components
Hooks: chart counter, script logger, phase validator (configured in .claude/settings.json)
Skills: /interpret (finding format), /publish-finding (Notion push)
Agent: country-profiler (parallel country analysis)

## Technical Notes
Technical note: the Notion MCP server is defined in .mcp.json (not in .claude/settings.json) because this version of Claude Code requires project-scoped MCP servers to live in that separate file — the mcpServers key is silently ignored if placed inside settings.json. settings.json therefore contains only the 3 hooks (chart counter, script logger, and phase validator); the Notion connection is configured and verified independently via .mcp.json and confirmed working with `claude mcp list`.