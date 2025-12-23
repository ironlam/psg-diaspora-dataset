# Data Collection Strategy - Phase 1

## Overview

Phase 1 focuses on building a comprehensive dataset of professional footballers with ties to Île-de-France, born between 1980-2006.

**Estimated population**: 500-1000 players meeting our criteria

---

## Collection Pipeline

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   1. SEED LIST   │────▶│  2. ENRICHMENT   │────▶│  3. VALIDATION   │
│                  │     │                  │     │                  │
│ - Wikidata query │     │ - Transfermarkt  │     │ - Cross-check    │
│ - Known players  │     │ - FBRef          │     │ - Deduplication  │
│ - Club histories │     │ - Wikipedia      │     │ - Quality score  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

---

## Step 1: Build Seed List

### 1.1 Wikidata SPARQL Query

Wikidata is our primary source for birthplace data. It's free, structured, and allows SPARQL queries.

```sparql
# Players born in Île-de-France, born 1980-2006
SELECT ?player ?playerLabel ?birthDate ?birthPlaceLabel ?nationalityLabel
WHERE {
  ?player wdt:P106 wd:Q937857 .          # occupation: football player
  ?player wdt:P19 ?birthPlace .           # has birthplace
  ?birthPlace wdt:P131* wd:Q13917 .       # in Île-de-France (recursive)
  ?player wdt:P569 ?birthDate .           # has birth date

  FILTER(YEAR(?birthDate) >= 1980 && YEAR(?birthDate) <= 2006)

  OPTIONAL { ?player wdt:P27 ?nationality }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en" }
}
ORDER BY ?birthDate
```

**Expected yield**: 300-500 players

### 1.2 Club-Based Collection

For players who might not be in Wikidata, collect from club histories:

1. **PSG academy alumni** (Transfermarkt youth squad archives)
2. **Paris FC alumni**
3. **Red Star FC alumni**
4. **Clairefontaine graduates** (INF lists)

### 1.3 Manual Additions

Known players who may be missed:
- Create `data/external/manual_seed_players.csv` with verified players

---

## Step 2: Data Enrichment

For each player in seed list, collect:

### From Transfermarkt

| Field | Priority | Notes |
|-------|----------|-------|
| Full name | High | For matching |
| Date of birth | High | Verification |
| Birthplace (city) | High | Core data |
| Nationality/ies | High | Diaspora indicator |
| Current club | Medium | |
| Market value | Medium | Success proxy |
| Career history | High | For trajectory analysis |
| Youth clubs | High | Training location |

### From FBRef

| Field | Priority | Notes |
|-------|----------|-------|
| Appearances by competition | High | For success tiers |
| National team caps | High | Tier 4 criteria |
| Statistics | Low | Not primary focus |

### From Wikipedia/Wikidata

| Field | Priority | Notes |
|-------|----------|-------|
| Parents' origin | Medium | If mentioned |
| Exact birthplace (commune) | High | For mapping |
| Coordinates | Medium | For visualization |

---

## Step 3: Validation & Quality

### Deduplication

Players may appear multiple times with:
- Different name spellings (accents, transliteration)
- Different IDs across sources

**Solution**: Fuzzy matching on name + DOB

### Quality Score

Each player record gets a quality score (0-1):

```python
quality_score = (
    0.3 * has_birthplace +
    0.2 * has_career_history +
    0.2 * has_youth_clubs +
    0.2 * has_nationality +
    0.1 * has_statistics
)
```

### Cross-Validation

- Compare Transfermarkt birthplace with Wikidata
- Flag discrepancies for manual review

---

## Data Collection Tools

### Option A: Wikidata (Recommended Start)

**Pros**: Free, legal, structured, birthplace data
**Cons**: Not all players included

```bash
# Query Wikidata
python src/collectors/wikidata.py --query players_idf --output data/raw/wikidata_players.json
```

### Option B: soccerdata Package

**Pros**: Easy to use, multiple sources
**Cons**: Limited to recent seasons, no birthplace

```python
import soccerdata as sd
fbref = sd.FBref(leagues="FRA-Ligue 1", seasons=2023)
players = fbref.read_player_season_stats()
```

### Option C: Manual Scraping (Last Resort)

**Pros**: Complete data
**Cons**: Legal grey area, time-consuming, may break

---

## Estimated Timeline

| Task | Effort | Output |
|------|--------|--------|
| Wikidata query | 1 day | 300-500 players |
| Enrich from Transfermarkt | 3-5 days | Career data |
| Enrich from FBRef | 2-3 days | Statistics |
| Validation & cleaning | 2-3 days | Final dataset |
| **Total** | **~2 weeks** | **500-1000 players** |

---

## Output Schema

Final dataset: `data/processed/players_idf.parquet`

```python
{
    "player_id": "uuid",
    "name": "string",
    "full_name": "string",
    "date_of_birth": "date",

    # Geography
    "birthplace_city": "string",
    "birthplace_department": "string",  # 75, 93, etc.
    "birthplace_lat": "float",
    "birthplace_lon": "float",

    # Origins
    "nationalities": ["string"],
    "is_dual_national": "bool",
    "african_nationality": "string | null",
    "diaspora_region": "string | null",  # Sub-Saharan, Maghreb, Overseas, None

    # Career
    "youth_clubs": ["string"],
    "psg_academy": "bool",
    "career_clubs": [{
        "club": "string",
        "country": "string",
        "start_year": "int",
        "end_year": "int",
        "appearances": "int",
        "is_youth": "bool"
    }],

    # Success metrics
    "total_pro_appearances": "int",
    "top5_league_appearances": "int",
    "national_team_caps": "int",
    "success_tier": "int",  # 1-4

    # Metadata
    "data_sources": ["string"],
    "quality_score": "float",
    "last_updated": "date"
}
```

---

## Next Steps

1. [ ] Create Wikidata collector script
2. [ ] Run initial query, assess yield
3. [ ] Decide on Transfermarkt approach (manual vs scraped vs Kaggle)
4. [ ] Build enrichment pipeline
5. [ ] Create validation/dedup logic
