# Article Draft: Franciliens et PSG - Part 2: The Data

*This is a draft outline for the Medium article. Fill in with your voice and perspective.*

---

## Title Options

1. "Franciliens et PSG : une histoire de migrations, de quartiers et de football (Partie 2) - Les données"
2. "40% de la diaspora africaine : ce que les données révèlent sur le vivier francilien"
3. "713 footballeurs, une région : analyse du vivier Île-de-France"

---

## Structure

### I. Introduction (200 words)

**Hook**: Dans la première partie, nous avons exploré le contexte sociologique. Maintenant, passons aux données.

**Key stat to lead with**: Sur 713 footballeurs professionnels nés en Île-de-France entre 1980 et 2006, 40.5% ont un lien avec la diaspora africaine.

**What this article covers**:
- Méthodologie de collecte
- Répartition géographique
- Analyse de la diaspora
- Tendances temporelles
- Limites et perspectives

---

### II. Méthodologie (300 words)

**Data source**: Wikidata (SPARQL queries)

**Criteria**:
- Footballeurs professionnels (P106 = Q937857)
- Nés en Île-de-France (8 départements)
- Années de naissance: 1980-2006

**Limitations to acknowledge**:
- Manque les 93 et 95 (rate limit) - EN COURS DE RÉSOLUTION
- Seuls les joueurs avec entrée Wikidata
- Lieu de naissance ≠ lieu de formation

**Code available**: Lien vers GitHub

---

### III. Les chiffres clés (400 words)

**Insert infographic here**: `docs/figures/summary_infographic.png`

#### 3.1 Vue d'ensemble

| Métrique | Valeur |
|----------|--------|
| Total joueurs | 713 |
| Bi-nationaux | 37.9% |
| Diaspora africaine | 40.5% |

#### 3.2 Répartition par région d'origine

**Insert chart**: `diaspora_regions_pie.png`

- Afrique subsaharienne: 26.9%
- Maghreb: 9.0%
- Portugal: 1.4%
- Caraïbes/Outre-mer: 1.1%

**Commentary**: La prédominance de l'Afrique subsaharienne reflète les vagues migratoires des années 1970-80...

#### 3.3 Top pays d'origine

**Insert chart**: `top_countries_bar.png`

1. RD Congo: 41
2. Mali: 39
3. Sénégal: 29
4. Algérie: 28
5. Côte d'Ivoire: 25

**Commentary**: Ces pays correspondent aux principales communautés immigrées en Île-de-France...

---

### IV. Répartition géographique (300 words)

**Insert chart**: `departments_bar.png`

**Note importante**: Les données pour la Seine-Saint-Denis (93) et le Val-d'Oise (95) sont en cours de collecte.

**Observations préliminaires**:
- Val-de-Marne (94): 171 joueurs
- Hauts-de-Seine (92): 165 joueurs
- Paris (75): 113 joueurs

**À venir**: Carte interactive avec les lieux de naissance précis

---

### V. Évolution temporelle (200 words)

**Insert chart**: `birth_years_trend.png`

**Peak periods**: 1990-1999 (321 joueurs sur 713 = 45%)

**Interpretation**: Cette génération correspond aux enfants nés de parents arrivés dans les années 1970-80...

---

### VI. Limites et prochaines étapes (200 words)

**Ce que ces données ne disent pas**:
- Corrélation ≠ causalité
- Lieu de naissance ≠ lieu de formation
- Réussite des joueurs (statistiques de carrière à venir)

**Prochaines analyses**:
- Enrichissement avec Transfermarkt (carrières)
- Analyse NLP de la couverture médiatique
- Comparaison avec d'autres régions (Londres, São Paulo)

---

### VII. Conclusion (150 words)

**Key takeaway**: L'Île-de-France produit un vivier exceptionnel, profondément lié à son histoire migratoire.

**Call to action**:
- Dataset disponible sur HuggingFace
- Code source sur GitHub
- Contributions bienvenues

---

## Visual Assets

| Chart | File | Usage |
|-------|------|-------|
| Summary infographic | `summary_infographic.png` | Header/social |
| Diaspora pie | `diaspora_regions_pie.png` | Section III |
| Top countries | `top_countries_bar.png` | Section III |
| Departments | `departments_bar.png` | Section IV |
| Birth years | `birth_years_trend.png` | Section V |
| Dual nationality | `dual_nationality_donut.png` | Optional |

---

## Social Media Snippets

### Twitter/X
```
📊 Nouvelle analyse: 713 footballeurs pros nés en Île-de-France (1980-2006)

• 40.5% diaspora africaine
• 37.9% bi-nationaux
• Top origines: RD Congo, Mali, Sénégal

Dataset + code: [lien]

#Football #Data #PSG #IleDeFrance
```

### LinkedIn
```
🔍 J'ai analysé les données de 713 footballeurs professionnels nés en Île-de-France.

Les résultats confirment ce que beaucoup pressentaient: le vivier francilien est profondément lié à l'histoire migratoire de la région.

40.5% ont un lien avec la diaspora africaine.

Dataset open source disponible.

[lien article]
```

---

## Notes for Writing

1. **Ton**: Factuel, documenté, accessible
2. **Public**: Fans de foot, data enthusiasts, sociologues
3. **Éviter**: Généralisations, essentialisme, conclusions causales
4. **Inclure**: Limites méthodologiques, nuances, perspectives futures
