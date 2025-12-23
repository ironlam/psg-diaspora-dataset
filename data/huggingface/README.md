---
license: cc-by-4.0
task_categories:
  - tabular-classification
  - tabular-regression
language:
  - fr
  - en
tags:
  - football
  - soccer
  - france
  - demographics
  - migration
  - sports
  - paris
  - ile-de-france
size_categories:
  - n<1K
---

# Île-de-France Professional Footballers Dataset

A dataset of professional football players born in the Île-de-France region (Greater Paris) between 1980 and 2006.

## Dataset Description

This dataset explores the relationship between the Île-de-France region's demographic composition and its exceptional football talent production. The region is widely considered one of the world's largest pools of professional football talent.

### Key Statistics

- **713** professional footballers
- **37.9%** are dual nationals
- **40.5%** have African diaspora background

### Diaspora Breakdown

| Region | Players | % of Total |
|--------|---------|------------|
| Sub-Saharan Africa | 192 | 26.9% |
| Maghreb | 64 | 9.0% |
| Portugal | 10 | 1.4% |
| Caribbean/Overseas | 8 | 1.1% |
| Other Europe | 7 | 1.0% |

### Top Origin Countries (besides France)

1. DR Congo: 41
2. Mali: 39
3. Senegal: 29
4. Algeria: 28
5. Ivory Coast: 25

## Dataset Structure

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `wikidata_id` | string | Wikidata entity ID (e.g., Q12345) |
| `name` | string | Player's name |
| `birth_date` | string | Date of birth (YYYY-MM-DD) |
| `birth_year` | int | Year of birth |
| `birth_city` | string | City of birth |
| `birth_department` | string | French département code (75, 92, 93, etc.) |
| `nationalities` | list | List of nationalities |
| `is_dual_national` | bool | Whether player has multiple nationalities |
| `diaspora_region` | string | Diaspora region (Sub-Saharan Africa, Maghreb, etc.) |
| `diaspora_countries` | list | Specific diaspora countries |

### Data Files

- `idf_footballers.csv` - CSV format
- `idf_footballers.parquet` - Parquet format (recommended)
- `idf_footballers.jsonl` - JSON Lines format

## Limitations

⚠️ **Important limitations to consider:**

1. **Missing data**: Seine-Saint-Denis (93) and Val-d'Oise (95) départements have 0 entries due to Wikidata rate limiting during collection. These are among the most productive départements for football talent.

2. **Selection bias**: Only players with Wikidata entries are included. Lesser-known professional players may be missing.

3. **Birthplace ≠ Training location**: A player born in a location may have been raised or trained elsewhere.

4. **Diaspora identification**: Based on nationality data, which may not capture all players with diaspora backgrounds.

## Data Sources

- **Wikidata**: Primary source for biographical data
- Collection date: 2024-12-24

## Use Cases

- Analysis of regional football talent production
- Study of migration patterns and sports
- Demographic research
- Sports sociology research

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{idf_footballers_2024,
  title={Île-de-France Professional Footballers Dataset},
  author={Diaby, Lamine},
  year={2024},
  url={https://huggingface.co/datasets/ldiaby/idf-footballers}
}
```

## License

This dataset is released under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).

## Contact

For questions or contributions, please open an issue on the [GitHub repository](https://github.com/ldiaby/psg-diaspora-dataset).
