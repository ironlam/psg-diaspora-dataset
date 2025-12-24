# Project Status

**Generated automatically during overnight session**

## Current State: Ready for Publication (pending 93/95 data)

### Data Collection Status

| Département | Code | Players | Status |
|-------------|------|---------|--------|
| Paris | 75 | 113 | Complete |
| Hauts-de-Seine | 92 | 165 | Complete |
| Val-de-Marne | 94 | 171 | Complete |
| Yvelines | 78 | 88 | Complete |
| Seine-et-Marne | 77 | 48 | Complete |
| Essonne | 91 | 44 | Complete |
| **Seine-Saint-Denis** | **93** | **0** | **PENDING** |
| **Val-d'Oise** | **95** | **0** | **PENDING** |

**Total (current)**: 713 players

### Analysis Summary

```
┌─────────────────────────────────────────────────────────────┐
│ KEY FINDINGS                                                │
├─────────────────────────────────────────────────────────────┤
│ Total players:         713                                  │
│ Dual nationals:        270 (37.9%)                          │
│ African diaspora:      289 (40.5%)                          │
├─────────────────────────────────────────────────────────────┤
│ TOP ORIGINS                                                 │
│ 1. DR Congo:    41                                          │
│ 2. Mali:        39                                          │
│ 3. Senegal:     29                                          │
│ 4. Algeria:     28                                          │
│ 5. Ivory Coast: 25                                          │
└─────────────────────────────────────────────────────────────┘
```

### Git Commits

```
7100158 Add HuggingFace upload script
553782d Add GitHub Actions CI and Makefile
cdc9776 Add documentation, tests, and article draft
1f5ebcc Add visualizations, retry script, and morning summary
aa94c81 Initial commit: IDF footballers dataset (713 players)
```

### Files Ready

**Documentation**:
- README.md (with charts)
- CONTRIBUTING.md
- METHODOLOGY.md
- DATA_COLLECTION_STRATEGY.md
- ARTICLE_DRAFT.md

**Data**:
- data/huggingface/ (CSV, Parquet, JSONL)
- data/processed/analysis_results.json
- data/processed/article_stats.md

**Visualizations** (in docs/figures/):
- summary_infographic.png
- diaspora_regions_pie.png
- top_countries_bar.png
- birth_years_trend.png
- departments_bar.png
- dual_nationality_donut.png

**Scripts**:
- scripts/retry_93_95.py
- scripts/upload_huggingface.py

**Tests**:
- 8 tests passing

### Next Steps

1. **Collect 93/95 data**: `make retry-93-95`
2. **Push to GitHub**: `gh repo create psg-diaspora-dataset --public --source=. --push`
3. **Upload to HuggingFace**: `./venv/bin/python scripts/upload_huggingface.py`
4. **Write Medium article**: Use docs/ARTICLE_DRAFT.md as template

### Rate Limit Status

Wikidata rate limit active. Typically clears after:
- Light limits: 15-30 minutes
- Heavy limits: 1-2 hours

To check:
```bash
curl -s -o /dev/null -w "%{http_code}" "https://query.wikidata.org/sparql?query=SELECT%20*%20WHERE%20%7B%20%3Fs%20%3Fp%20%3Fo%20%7D%20LIMIT%201"
```
If returns 200, rate limit cleared.
