# Methodology

## Research Focus

**Primary Question**: What is the relationship between African diaspora presence in Île-de-France and the region's exceptional football talent production?

**Secondary Questions**:
1. Which départements/communes produce the most professional players?
2. How does media discourse frame players from diaspora backgrounds?
3. Has PSG's formation strategy evolved to better leverage this local talent pool?

---

## Scope Definition

### Temporal Scope

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Birth years | 1980-2006 | Captures 2nd and 3rd generation of post-1960s African migration |
| Career data | 1998-2024 | France 98 as symbolic milestone; includes Qatar era |

### Geographic Scope

**Phase 1** (Current): Île-de-France only
- 8 départements (75, 77, 78, 91, 92, 93, 94, 95)
- ~12 million inhabitants
- ~1,200 amateur clubs

**Phase 2** (Future): Add Greater London for comparison
- Similar post-colonial migration patterns
- Comparable urban density
- Strong academy system

---

## Player Population

### Inclusion Criteria

A player is included if ANY of these conditions are met:

1. **Born in Île-de-France** (primary)
2. **Trained at an IDF club** during formative years (U10-U17)
3. **Passed through PSG academy** at any point

AND meets minimum career threshold:
- At least 10 professional appearances OR
- Called up to any national team (including youth)

### Exclusion Criteria

- Players only briefly loaned to IDF clubs as professionals
- Players who moved to IDF after age 18 without prior training there

---

## Success Metrics (4-Tier Model)

We use a graduated definition of "success" to avoid binary thinking:

```
┌─────────────────────────────────────────────────────────────┐
│ TIER 4: ELITE                                               │
│ Senior national team (any country) ≥1 cap                   │
│ Examples: Mbappé, Maignan, Kimpembe, Tchouaméni             │
├─────────────────────────────────────────────────────────────┤
│ TIER 3: TOP LEAGUE                                          │
│ ≥10 appearances in Top 5 European league                    │
│ (Ligue 1, PL, La Liga, Bundesliga, Serie A)                 │
│ Examples: Diaby, Nkunku, Coman                              │
├─────────────────────────────────────────────────────────────┤
│ TIER 2: ESTABLISHED PRO                                     │
│ ≥50 professional appearances (any league)                   │
│ Includes Ligue 2, Championship, etc.                        │
├─────────────────────────────────────────────────────────────┤
│ TIER 1: PROFESSIONAL                                        │
│ ≥10 professional appearances                                │
│ Base threshold for "made it"                                │
└─────────────────────────────────────────────────────────────┘
```

### Why This Model?

- **Avoids survivorship bias**: We don't only count superstars
- **Captures different levels**: A Ligue 2 career is still professional
- **Measurable**: Clear, objective criteria
- **Comparable**: Can apply same tiers to any region

---

## Diaspora Identification

### Challenge

France does not collect ethnic statistics. We cannot directly identify "African diaspora" players.

### Proxy Methods (with limitations)

| Method | Reliability | Limitations |
|--------|-------------|-------------|
| **Dual nationality** | High | Not all have dual citizenship |
| **National team choice** | High | Only for those who played internationally |
| **Parents' birthplace** | High | Rarely available in public data |
| **Surname analysis** | Low | Risk of false positives/negatives |
| **Self-identification** | High | Only from interviews/media |

### Our Approach

1. **Primary**: Dual nationality + national team data (from Transfermarkt/FBRef)
2. **Secondary**: Media corpus analysis (mentions of origins, parents' country)
3. **Validation**: Cross-reference with interviews, Wikipedia

### Ethical Considerations

- We do NOT assign ethnicity based on names alone
- We report data with uncertainty ranges
- We acknowledge this is an approximation
- Focus is on structural patterns, not individual categorization

---

## Data Sources

### Player Data

| Source | Data Available | Limitations |
|--------|----------------|-------------|
| **Transfermarkt** | Career history, market value, transfers | ToS restrictions, scraping needed |
| **FBRef** | Detailed statistics, national team data | Mostly top leagues |
| **Wikidata** | Birthplace, nationality, structured data | Incomplete for lesser-known players |
| **FFF** | Licensed players by region | Aggregated only, no individual data |

### Demographic Data

| Source | Data Available | Format |
|--------|----------------|--------|
| **INSEE** | Population, immigration, income by commune | API + CSV |
| **INED** | Historical migration data | Reports + datasets |

### Media Corpus

| Source | Type | Access |
|--------|------|--------|
| **L'Équipe** | Sports daily | Web scraping |
| **Le Parisien** | Regional daily | Web scraping |
| **So Foot** | Sports magazine | Web scraping |
| **Le Monde** | National daily | Archive API |

---

## Analysis Plan

### Quantitative Analysis

1. **Geographic distribution**: Map birthplaces by département/commune
2. **Temporal trends**: Player production by birth cohort (1980s, 1990s, 2000s)
3. **Success rates**: % reaching each tier by origin area
4. **Correlation analysis**: Talent production vs demographics (density, immigration rate, poverty rate)

### NLP Analysis

1. **Keyword frequency**: How often are "quartiers", "origins", etc. mentioned?
2. **Sentiment analysis**: Is coverage positive/negative?
3. **Framing analysis**: What attributes are emphasized (physical vs technical)?
4. **Comparison**: Does coverage differ for diaspora vs non-diaspora players?

### Statistical Methods

- Descriptive statistics (means, distributions)
- Correlation analysis (Pearson, Spearman)
- Regression (controlling for confounders)
- Clustering (geographic patterns)

---

## Limitations

### Data Limitations

1. **Incomplete coverage**: Not all players have full data
2. **Selection bias**: More data on successful players
3. **Temporal gaps**: Older data less complete

### Methodological Limitations

1. **Cannot prove causation**: Only correlations
2. **Diaspora identification is imperfect**: Proxy methods have errors
3. **Media corpus is a sample**: Not exhaustive

### Scope Limitations

1. **Men's football only** (women's football deserves separate study)
2. **IDF focus**: Other regions (Lyon, Marseille) also produce talent
3. **Professional focus**: Ignores amateur/semi-pro careers

---

## Reproducibility

All code, data processing steps, and analysis will be:
- Version controlled (Git)
- Documented with docstrings and comments
- Runnable from scratch with `requirements.txt`
- Data sources cited with access dates
