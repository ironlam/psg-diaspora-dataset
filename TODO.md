# Project TODO

## High Priority

### Data Collection
- [ ] **Retry Seine-Saint-Denis (93) collection** - Rate limited on 2024-12-24
  - Wait ~1 hour and run: `./venv/bin/python src/collectors/wikidata.py`
  - Or query specific cities: Saint-Denis, Montreuil, Bondy, Aubervilliers, etc.

- [ ] **Retry Val-d'Oise (95) collection** - Rate limited on 2024-12-24
  - Same as above
  - Key cities: Argenteuil, Sarcelles, Cergy, Pontoise

### Data Enrichment
- [ ] Add Transfermarkt data for career statistics
- [ ] Add FBRef data for match statistics
- [ ] Cross-reference with FFF licensed players data

## Medium Priority

### Analysis
- [ ] Complete geographic analysis once 93/95 data is available
- [ ] Correlation with INSEE demographic data
- [ ] Career trajectory analysis

### Visualization
- [ ] Map of birthplaces by département
- [ ] Sankey diagram of career paths
- [ ] Timeline of player production by birth year

### Publication
- [ ] Finalize Hugging Face dataset
- [ ] Write Medium article (or Observable notebook)
- [ ] Prepare GitHub repository for public release

## Low Priority

- [ ] Add NLP analysis of media coverage
- [ ] Compare with Greater London (Phase 2)
- [ ] Build interactive web visualization

## Notes

### Rate Limit Recovery
Wikidata rate limit typically resets after:
- 1 hour for light limits
- 24 hours for heavy limits

To check if rate limit is cleared:
```bash
curl -I "https://query.wikidata.org/sparql?query=SELECT%20*%20WHERE%20%7B%20%3Fs%20%3Fp%20%3Fo%20%7D%20LIMIT%201"
```

If you get HTTP 200, you're good to retry.
