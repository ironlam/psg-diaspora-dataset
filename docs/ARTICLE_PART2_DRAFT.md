# Building a Football Players Dataset with Wikidata and Python

*How I collected 1,165 footballer profiles, analyzed diaspora patterns, and published to HuggingFace*

---

## TL;DR

I built an open dataset of professional footballers born in the Paris region (Île-de-France) using Wikidata SPARQL queries. The dataset includes birthplace, nationalities, and diaspora background for 1,165 players born between 1980-2006.

- **Dataset**: [HuggingFace - ldiaby/idf-footballers](https://huggingface.co/datasets/ldiaby/idf-footballers)
- **Code**: [GitHub - psg-diaspora-dataset](https://github.com/ldiaby/psg-diaspora-dataset)
- **Stack**: Python, SPARQL, Pandas, Matplotlib, HuggingFace Hub

---

## The Problem

I wanted to quantify something often discussed anecdotally: the relationship between migration patterns and football talent production in the Paris region. But there was no ready-made dataset.

**Requirements:**
- Birthplace at commune level (not just "Paris")
- Multiple nationalities (to identify diaspora backgrounds)
- Open data, legally usable
- Structured enough to query programmatically

---

## Why Wikidata?

Wikidata is the structured database behind Wikipedia. Every entity has a unique identifier (QID) and properties (PIDs).

**Relevant properties for this project:**
| Property | PID | Description |
|----------|-----|-------------|
| occupation | P106 | Filter for footballers (Q937857) |
| place of birth | P19 | Links to a location entity |
| date of birth | P569 | For filtering by year |
| country of citizenship | P27 | Can have multiple values |
| located in administrative entity | P131 | Hierarchical location data |

**Advantages:**
- Free API, no authentication required
- SPARQL endpoint for complex queries
- Community-maintained, reasonably accurate

**Limitations:**
- Only notable players have entries
- Data quality varies
- Rate limiting on heavy queries

---

## Data Collection Architecture

```
┌─────────────────┐     SPARQL      ┌─────────────────┐
│    Wikidata     │ ───────────────▶│  Python Client  │
│  SPARQL Endpoint│                 │    (httpx)      │
└─────────────────┘                 └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │   JSON Files    │
                                    │  (raw/wikidata) │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │    Analysis     │
                                    │    (Pandas)     │
                                    └────────┬────────┘
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                        ┌──────────┐  ┌──────────┐  ┌──────────┐
                        │   CSV    │  │ Parquet  │  │  JSONL   │
                        └──────────┘  └──────────┘  └──────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  HuggingFace    │
                                    │      Hub        │
                                    └─────────────────┘
```

---

## The SPARQL Query

The core query fetches footballers born in a specific département:

```sparql
SELECT DISTINCT
    ?player
    ?playerLabel
    ?birthDate
    ?birthPlace
    ?birthPlaceLabel
    (GROUP_CONCAT(DISTINCT ?nationalityLabel; separator=", ") AS ?nationalities)
WHERE {
    # Filter: professional footballer
    ?player wdt:P106 wd:Q937857 .

    # Filter: birthplace in target département
    ?player wdt:P19 ?birthPlace .
    {
        ?birthPlace wdt:P131 wd:Q12761 .  # Seine-Saint-Denis
    } UNION {
        ?birthPlace wdt:P131/wdt:P131 wd:Q12761 .
    } UNION {
        ?birthPlace wdt:P131/wdt:P131/wdt:P131 wd:Q12761 .
    }

    # Filter: birth year range
    ?player wdt:P569 ?birthDate .
    FILTER(YEAR(?birthDate) >= 1980 && YEAR(?birthDate) <= 2006)

    # Optional: nationalities
    OPTIONAL {
        ?player wdt:P27 ?nationality .
        ?nationality rdfs:label ?nationalityLabel .
        FILTER(LANG(?nationalityLabel) = "fr")
    }

    SERVICE wikibase:label {
        bd:serviceParam wikibase:language "fr,en" .
    }
}
GROUP BY ?player ?playerLabel ?birthDate ?birthPlace ?birthPlaceLabel
```

**Key techniques:**
- `UNION` for hierarchical location matching (commune → arrondissement → département)
- `GROUP_CONCAT` to aggregate multiple nationalities into one field
- `SERVICE wikibase:label` for automatic label resolution

---

## Handling Wikidata's Quirks

### Problem 1: Rate Limiting

Wikidata returns 429 or 403 when you query too aggressively.

**Solution:** Query by département instead of all Île-de-France at once, with delays:

```python
for dept_code in ["75", "92", "93", "94", "95", "77", "78", "91"]:
    players = collector.get_footballers_by_department(dept_code)
    all_players.extend(players)
    time.sleep(2)  # Be nice to the API
```

### Problem 2: Wrong Entity IDs

I initially used wrong QIDs for some départements. The fix was to verify each QID:

```sparql
SELECT ?label WHERE {
    wd:Q12761 rdfs:label ?label .
    FILTER(LANG(?label) = "fr")
} LIMIT 1
```

**Correct IDs for Île-de-France départements:**
| Département | QID |
|-------------|-----|
| Paris (75) | Q90 |
| Seine-et-Marne (77) | Q12753 |
| Yvelines (78) | Q12820 |
| Essonne (91) | Q12549 |
| Hauts-de-Seine (92) | Q12543 |
| Seine-Saint-Denis (93) | Q12761 |
| Val-de-Marne (94) | Q12788 |
| Val-d'Oise (95) | Q12784 |

### Problem 3: Timeout on Complex Queries

The recursive `wdt:P131*` pattern times out on large datasets.

**Solution:** Limit recursion depth with explicit UNION clauses (3 levels max).

---

## Data Processing Pipeline

### 1. Nationality Classification

To identify diaspora backgrounds, I mapped nationalities to regions:

```python
DIASPORA_MAPPING = {
    "Sub-Saharan Africa": [
        "Mali", "Sénégal", "Côte d'Ivoire", "Cameroun",
        "République démocratique du Congo", "Congo", "Guinée", ...
    ],
    "Maghreb": ["Algérie", "Maroc", "Tunisie"],
    "Caribbean/Overseas": ["Guadeloupe", "Martinique", "Guyane", ...],
    ...
}

def classify_diaspora(nationalities: list[str]) -> str | None:
    for region, countries in DIASPORA_MAPPING.items():
        if any(nat in countries for nat in nationalities):
            return region
    return None
```

### 2. Dual Nationality Detection

```python
def is_dual_national(nationalities: list[str]) -> bool:
    return len(nationalities) > 1
```

### 3. Department Extraction

Birthplace names don't include département codes. I extracted them from Wikidata location hierarchy or used a commune → département mapping.

---

## Dataset Schema

Final schema for HuggingFace:

```python
{
    "wikidata_id": "Q615",          # Unique identifier
    "name": "Kylian Mbappé",
    "date_of_birth": "1998-12-20",
    "birthplace": "Bondy",
    "birthplace_id": "Q217138",
    "department": "93",
    "nationalities": ["France", "Cameroun"],
    "is_dual_national": true,
    "diaspora_region": "Sub-Saharan Africa"
}
```

**Export formats:**
- CSV (universal compatibility)
- Parquet (efficient for large datasets, type-safe)
- JSONL (streaming, ML pipelines)

---

## Publishing to HuggingFace

```python
from huggingface_hub import HfApi

api = HfApi()
api.create_repo("ldiaby/idf-footballers", repo_type="dataset", exist_ok=True)
api.upload_folder(
    folder_path="data/huggingface",
    repo_id="ldiaby/idf-footballers",
    repo_type="dataset",
)
```

The dataset card (`README.md` in the data folder) follows HuggingFace's template with:
- Dataset description
- Data fields
- Collection methodology
- Limitations
- Citation info

---

## Visualizations

Generated with Matplotlib:

| Chart | Purpose |
|-------|---------|
| `diaspora_regions_pie.png` | Breakdown by origin region |
| `top_countries_bar.png` | Top 10 countries |
| `departments_bar.png` | Players by département |
| `birth_years_trend.png` | Temporal distribution |
| `dual_nationality_donut.png` | Dual vs single nationality |

Example code:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
departments = sorted(data.items(), key=lambda x: -x[1])
ax.barh([d[0] for d in departments], [d[1] for d in departments])
ax.set_xlabel("Number of Players")
ax.set_title("Professional Footballers by Département")
plt.savefig("departments_bar.png", bbox_inches="tight")
```

---

## Results Summary

| Metric | Value |
|--------|-------|
| Total players | 1,165 |
| Dual nationals | 39.4% |
| African diaspora | 42.5% |
| Top département | Seine-Saint-Denis (322) |
| Top origin country | Mali (78) |

---

## Potential ML Applications

This dataset could be used for:

1. **Geographic clustering**: Identify talent hotspots at commune level
2. **Time series analysis**: Predict future talent production based on demographic trends
3. **Network analysis**: Link players to clubs, training centers
4. **NLP**: Combine with media corpus to analyze coverage patterns
5. **Comparison models**: Similar datasets for London, São Paulo, etc.

---

## Limitations

- **Survivorship bias**: Only players with Wikipedia entries
- **Birthplace ≠ training location**: A player born in Bondy might have trained in Lyon
- **No performance metrics**: No goals, caps, market value (requires Transfermarkt enrichment)
- **Static snapshot**: Wikidata changes; dataset is frozen at collection date

---

## Reproduce This Project

```bash
git clone https://github.com/ldiaby/psg-diaspora-dataset
cd psg-diaspora-dataset
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Collect data
python src/collectors/wikidata.py

# Run analysis
python src/analysis/analyze_players.py

# Generate charts
python src/visualization/charts.py

# Run tests
pytest tests/ -v
```

---

## Next Steps

- [ ] Enrich with Transfermarkt data (career stats, market value)
- [ ] Build interactive visualization app (Streamlit/Plotly Dash)
- [ ] Compare with London dataset
- [ ] Add NLP analysis of media coverage

---

## Links

- **Dataset**: [HuggingFace](https://huggingface.co/datasets/ldiaby/idf-footballers)
- **Code**: [GitHub](https://github.com/ldiaby/psg-diaspora-dataset)
- **Author**: Lamine DIABY

---

*Tags: #Wikidata #SPARQL #Python #OpenData #HuggingFace #DataEngineering #Football*
