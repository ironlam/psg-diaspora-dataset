# Project Context - IDF Footballers Dataset

**Last updated**: 2025-01-04
**Purpose**: Preserve full context before conversation compacting

---

## Project Overview

**Goal**: Build a data-driven analysis of the relationship between Île-de-France's migration history and football talent production, to support a Medium article series.

**Author**: Lamine DIABY

**Repositories**:
- GitHub: `ldiaby/psg-diaspora-dataset` (not yet pushed)
- HuggingFace: `ldiaby/idf-footballers` (not yet uploaded)

---

## What Was Built

### 1. Data Collection Pipeline
- **Source**: Wikidata SPARQL queries
- **Script**: `src/collectors/wikidata.py`
- **Criteria**: Professional footballers (P106=Q937857), born in Île-de-France, years 1980-2006

**Département QIDs** (verified correct):
```python
DEPARTMENTS = {
    75: "Q90",        # Paris
    77: "Q12753",     # Seine-et-Marne
    78: "Q12820",     # Yvelines
    91: "Q12549",     # Essonne
    92: "Q12543",     # Hauts-de-Seine
    93: "Q12761",     # Seine-Saint-Denis (CORRECTED from Q13045343)
    94: "Q12788",     # Val-de-Marne
    95: "Q12784",     # Val-d'Oise (CORRECTED from Q14212344)
}
```

### 2. Analysis Pipeline
- **Script**: `src/analysis/analyze_players.py`
- **Output**: `data/processed/analysis_results.json`, `data/processed/article_stats.md`
- **Features**: Diaspora categorization, dual nationality detection, department extraction from birthplace names

### 3. Visualization
- **Static charts**: `src/visualization/charts.py` → `docs/figures/`
- **Interactive app**: `app/app.py` (Streamlit)
- **Run with**: `make app` or `./venv/bin/streamlit run app/app.py`

### 4. HuggingFace Dataset
- **Location**: `data/huggingface/`
- **Formats**: CSV, Parquet, JSONL
- **Schema**: wikidata_id, name, birth_date, birth_year, birth_department, nationalities, is_dual_national, diaspora_region, diaspora_countries, birth_city

---

## Key Results

| Metric | Value |
|--------|-------|
| Total players | 1,165 |
| Dual nationals | 39.4% (459) |
| African diaspora | 42.5% (495) - **LOWER BOUND** |
| Top département | Seine-Saint-Denis (93): 316 players |
| Top origin country | Mali (78) |

**Players by département**:
- 93 Seine-Saint-Denis: 316
- 92 Hauts-de-Seine: 188
- 94 Val-de-Marne: 184
- 95 Val-d'Oise: 136
- 75 Paris: 112
- 78 Yvelines: 91
- 77 Seine-et-Marne: 49
- 91 Essonne: 0 (not collected - QID issue or no data)
- Unknown: 89

---

## Critical Methodological Limitation

### Citizenship ≠ Heritage

Wikidata records **legal citizenships**, not ancestry. This **underestimates** diaspora connections.

**Examples**:
| Player | Wikidata shows | Reality |
|--------|----------------|---------|
| Kylian Mbappé | France + Cameroon | Mother also **Algerian** (not captured) |
| Paul Pogba | France only | **Both parents from Guinea** |
| N'Golo Kanté | France only | **Parents from Mali** |

**Implication**: 42.5% is a floor. Actual heritage-based figure likely **60%+**.

### Birthplace ≠ Childhood

Mbappé recorded as born in Paris 19e, but **grew up in Bondy (93)**.

---

## Issues Encountered & Resolved

### 1. Wrong Wikidata QIDs for 93/95
- **Problem**: Initial QIDs (Q13045343, Q14212344) returned 0 results
- **Solution**: User manually verified correct QIDs on query.wikidata.org
- **Correct QIDs**: 93=Q12761, 95=Q12784

### 2. Wikidata Rate Limiting
- **Problem**: 403/429 errors during collection
- **Solution**: Query by département instead of all IDF, add delays between queries, proper User-Agent header

### 3. Department extraction failing
- **Problem**: 194 players had NaN department
- **Cause**: Players from 93/95 had `department` field set during collection, but analysis only looked at birthplace name
- **Solution**: Check `player.get('department')` first, then fallback to birthplace extraction
- **Result**: Reduced to 89 NaN

### 4. App type errors
- **Problem**: "93.0 - 93.0" instead of "93 - Seine-Saint-Denis"
- **Cause**: Department stored as float, not int
- **Solution**: `df['birth_department'] = df['birth_department'].astype(int)` after dropping NaN

### 5. Deprecated APIs
- **Streamlit**: `use_container_width=True` → `width='stretch'`
- **Plotly**: `scatter_mapbox` → `scatter_map`, `mapbox_style` → `map_style`

---

## File Structure

```
psg-diaspora-dataset/
├── app/
│   └── app.py                 # Streamlit interactive app
├── data/
│   ├── raw/wikidata/
│   │   ├── idf_footballers.json      # Main dataset (1165 players)
│   │   └── idf_footballers_93_95.json # 93/95 separate collection
│   ├── processed/
│   │   ├── analysis_results.json
│   │   └── article_stats.md
│   └── huggingface/
│       ├── README.md          # Dataset card
│       ├── idf_footballers.csv
│       ├── idf_footballers.parquet
│       └── idf_footballers.jsonl
├── docs/
│   ├── figures/               # 6 PNG charts
│   ├── ARTICLE_PART2_DRAFT.md # Technical article for developers
│   └── SOCIOLOGICAL_ARTICLE_IDEA.md # Pitch for sociology article
├── src/
│   ├── collectors/
│   │   └── wikidata.py        # Data collection
│   ├── analysis/
│   │   └── analyze_players.py # Analysis pipeline
│   └── visualization/
│       └── charts.py          # Static chart generation
├── scripts/
│   ├── retry_93_95.py         # Retry script for 93/95
│   └── upload_huggingface.py  # HF upload script
├── tests/
│   └── test_data.py           # 8 tests (all passing)
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions CI
├── Makefile                   # Common commands
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── METHODOLOGY.md
├── PROJECT_STATUS.md
├── MORNING_SUMMARY.md
└── CONTEXT.md                 # This file
```

---

## Git History

```
35b5655 Add citizenship vs heritage limitation to articles
3a2dac4 Fix app and add methodology explanations
1822a31 Add Streamlit visualization app
ae3d9a1 Add Seine-Saint-Denis (93) and Val-d'Oise (95) data
7549a35 Add PROJECT_STATUS.md with comprehensive status
ea21a7b Update morning summary with current status
7100158 Add HuggingFace upload script
553782d Add GitHub Actions CI and Makefile
cdc9776 Add documentation, tests, and article draft
1f5ebcc Add visualizations, retry script, and morning summary
aa94c81 Initial commit: IDF footballers dataset (713 players)
```

---

## Remaining Tasks

### To Publish
1. **Push to GitHub**: `gh repo create psg-diaspora-dataset --public --source=. --push`
2. **Upload to HuggingFace**: `huggingface-cli upload ldiaby/idf-footballers data/huggingface --repo-type dataset`

### Articles to Write
1. **Technical article** (for developers): `docs/ARTICLE_PART2_DRAFT.md` - nearly complete
2. **Sociological article** (for general public): `docs/SOCIOLOGICAL_ARTICLE_IDEA.md` - outline only

### Future Enhancements
- Collect Essonne (91) data - currently 0 players
- Enrich with Transfermarkt data (career stats, market value)
- Add NLP analysis of media coverage
- Compare with London dataset
- Build more advanced visualization app
- Deploy Streamlit app to cloud

---

## Commands Reference

```bash
# Setup
make setup                    # Create venv and install deps

# Run
make app                      # Start Streamlit app
make analyze                  # Run analysis pipeline
make charts                   # Generate static charts
make test                     # Run tests

# Data collection
./venv/bin/python src/collectors/wikidata.py    # Full collection
./venv/bin/python scripts/retry_93_95.py        # Retry 93/95 only

# Publish
gh repo create psg-diaspora-dataset --public --source=. --push
huggingface-cli upload ldiaby/idf-footballers data/huggingface --repo-type dataset
```

---

## Key Decisions Made

1. **Focus on Île-de-France only** (not comparing with London yet)
2. **Birth years 1980-2006** to capture active/recent professionals
3. **Use Wikidata** as primary source (legal, structured, free)
4. **Acknowledge limitations** rather than overclaim (citizenship ≠ heritage)
5. **Two-article approach**: Technical (for devs) + Sociological (for general public)
6. **Interactive app** for data exploration

---

## User Preferences Noted

- Don't add Claude Code mentions in git commits
- Focus on African diaspora specifically
- Want a "nice application" for visualization
- Articles should be less emotional, more explanatory
- Target audience for technical article: developers interested in AI, ML, data viz, HuggingFace

---

*This file preserves context for conversation continuity.*
