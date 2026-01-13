---
title: IDF Footballers Explorer
emoji: ⚽
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
tags:
  - football
  - france
  - wikidata
  - demographics
  - sports-analytics
  - streamlit
---

# IDF Footballers Dataset Explorer

Interactive exploration of **1,165 professional footballers** born in the Paris region (Île-de-France) between 1980 and 2006.

## Key Findings

| Metric | Value |
|--------|-------|
| Total players | 1,165 |
| Dual nationals | 39.4% |
| African diaspora* | 42.5% |
| Top département | Seine-Saint-Denis (316) |
| Top origin country | Mali (78) |

*Based on citizenship only — actual heritage is higher.

## Features

- **Filter** by department, diaspora region, birth year, nationality status
- **Interactive map** of Île-de-France with player distribution
- **Charts**: department breakdown, diaspora regions, birth year trends, top origin countries
- **Search** players by name
- **Download** filtered data as CSV

## Data Source

Data collected from [Wikidata](https://www.wikidata.org) using SPARQL queries.

## Important Limitations

- **Citizenship ≠ Heritage**: Wikidata records legal nationality, not ancestry. Paul Pogba appears as "French only" despite Guinean parents.
- **Birthplace ≠ Childhood**: Players are mapped to birth location, not where they grew up.
- **Coverage bias**: Only players notable enough for Wikipedia/Wikidata are included.

## Links

- **Dataset**: [HuggingFace](https://huggingface.co/datasets/ironlam/idf-footballers)
- **Code**: [GitHub](https://github.com/ironlam/psg-diaspora-dataset)
- **Article**: [Medium - Franciliens et PSG](https://medium.com/@diaby.lamine)

## Author

Built by **Lamine DIABY**
