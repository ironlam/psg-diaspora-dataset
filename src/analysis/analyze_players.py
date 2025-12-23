"""
Comprehensive analysis of Île-de-France footballers dataset.

This script produces:
1. Statistical summaries for the Medium article
2. Cleaned dataset for Hugging Face
3. Data exports for visualizations
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd


def load_data(filepath: Path) -> list[dict]:
    """Load player data from JSON."""
    with open(filepath) as f:
        data = json.load(f)
    return data.get("players", data)


def extract_department_from_birthplace(birthplace_name: str) -> str | None:
    """
    Extract département from birthplace name.
    This is approximate - based on known patterns.
    """
    name = birthplace_name.lower()

    # Paris arrondissements
    if "arrondissement de paris" in name or "paris" in name:
        return "75"

    # Known city -> département mappings (partial)
    city_to_dept = {
        "boulogne-billancourt": "92",
        "nanterre": "92",
        "colombes": "92",
        "asnières": "92",
        "courbevoie": "92",
        "rueil-malmaison": "92",
        "issy-les-moulineaux": "92",
        "levallois-perret": "92",
        "neuilly-sur-seine": "92",
        "antony": "92",
        "clichy": "92",
        "clamart": "92",
        "meudon": "92",
        "montrouge": "92",
        "suresnes": "92",
        "gennevilliers": "92",
        "châtillon": "92",
        "sceaux": "92",
        "puteaux": "92",
        "vanves": "92",
        "garches": "92",
        "chaville": "92",
        "fontenay-aux-roses": "92",
        "le plessis-robinson": "92",
        "bagneux": "92",
        "châtenay-malabry": "92",
        "créteil": "94",
        "vitry-sur-seine": "94",
        "champigny-sur-marne": "94",
        "saint-maur-des-fossés": "94",
        "ivry-sur-seine": "94",
        "maisons-alfort": "94",
        "fontenay-sous-bois": "94",
        "villejuif": "94",
        "vincennes": "94",
        "alfortville": "94",
        "choisy-le-roi": "94",
        "le kremlin-bicêtre": "94",
        "nogent-sur-marne": "94",
        "thiais": "94",
        "cachan": "94",
        "charenton-le-pont": "94",
        "orly": "94",
        "villeneuve-saint-georges": "94",
        "arcueil": "94",
        "fresnes": "94",
        "sucy-en-brie": "94",
        "joinville-le-pont": "94",
        "saint-mandé": "94",
        "versailles": "78",
        "sartrouville": "78",
        "mantes-la-jolie": "78",
        "saint-germain-en-laye": "78",
        "poissy": "78",
        "conflans-sainte-honorine": "78",
        "montigny-le-bretonneux": "78",
        "les mureaux": "78",
        "plaisir": "78",
        "trappes": "78",
        "houilles": "78",
        "chatou": "78",
        "le chesnay": "78",
        "carrières-sous-poissy": "78",
        "élancourt": "78",
        "rambouillet": "78",
        "meaux": "77",
        "chelles": "77",
        "melun": "77",
        "pontault-combault": "77",
        "savigny-le-temple": "77",
        "torcy": "77",
        "roissy-en-brie": "77",
        "combs-la-ville": "77",
        "villeparisis": "77",
        "ozoir-la-ferrière": "77",
        "dammarie-les-lys": "77",
        "lagny-sur-marne": "77",
        "évry": "91",
        "corbeil-essonnes": "91",
        "massy": "91",
        "savigny-sur-orge": "91",
        "sainte-geneviève-des-bois": "91",
        "athis-mons": "91",
        "palaiseau": "91",
        "viry-châtillon": "91",
        "vigneux-sur-seine": "91",
        "grigny": "91",
        "brunoy": "91",
        "les ulis": "91",
        "longjumeau": "91",
        "ris-orangis": "91",
        # 93 cities (for when we get the data)
        "saint-denis": "93",
        "montreuil": "93",
        "aubervilliers": "93",
        "aulnay-sous-bois": "93",
        "drancy": "93",
        "noisy-le-grand": "93",
        "pantin": "93",
        "bondy": "93",
        "bobigny": "93",
        "le blanc-mesnil": "93",
        "sevran": "93",
        "épinay-sur-seine": "93",
        "livry-gargan": "93",
        "clichy-sous-bois": "93",
        "stains": "93",
        "rosny-sous-bois": "93",
        "villepinte": "93",
        "la courneuve": "93",
        "le raincy": "93",
        "gagny": "93",
        "neuilly-sur-marne": "93",
        "pierrefitte-sur-seine": "93",
        "tremblay-en-france": "93",
        "villemomble": "93",
        "bagnolet": "93",
        "les lilas": "93",
        "romainville": "93",
        # 95 cities
        "argenteuil": "95",
        "sarcelles": "95",
        "cergy": "95",
        "garges-lès-gonesse": "95",
        "goussainville": "95",
        "franconville": "95",
        "bezons": "95",
        "villiers-le-bel": "95",
        "ermont": "95",
        "pontoise": "95",
        "herblay": "95",
        "taverny": "95",
        "saint-ouen-l'aumône": "95",
        "eaubonne": "95",
        "montmorency": "95",
        "enghien-les-bains": "95",
        "deuil-la-barre": "95",
        "cormeilles-en-parisis": "95",
        "saint-gratien": "95",
        "soisy-sous-montmorency": "95",
    }

    for city, dept in city_to_dept.items():
        if city in name:
            return dept

    return None


def categorize_diaspora(nationalities: list[str]) -> dict:
    """
    Categorize a player's diaspora background.
    Returns dict with region and countries.
    """
    sub_saharan = {
        "Mali", "Sénégal", "Côte d'Ivoire", "Cameroun", "Guinée",
        "République démocratique du Congo", "République du Congo",
        "Togo", "Gabon", "Bénin", "Ghana", "Nigeria", "Burkina Faso",
        "République centrafricaine", "Cap-Vert", "Guinée-Bissau",
        "Madagascar", "Maurice", "Guinée équatoriale", "Gambie",
        "Sierra Leone", "Liberia", "Niger", "Tchad", "Mauritanie",
        "Éthiopie", "Érythrée", "Somalie", "Kenya", "Ouganda",
        "Rwanda", "Burundi", "Tanzanie", "Zambie", "Zimbabwe",
        "Mozambique", "Angola", "Namibie", "Botswana", "Afrique du Sud",
        "Malawi", "Soudan", "Soudan du Sud"
    }

    maghreb = {"Algérie", "Maroc", "Tunisie", "Libye", "Égypte"}

    overseas = {
        "Guadeloupe", "Martinique", "Guyane", "Réunion", "Mayotte",
        "Haïti", "République dominicaine", "Jamaïque", "Trinité-et-Tobago",
        "Sainte-Lucie", "Dominique", "Grenade", "Barbade", "Antigua-et-Barbuda"
    }

    comoros = {"Comores"}

    portugal = {"Portugal"}

    other_europe = {
        "Espagne", "Italie", "Pologne", "Roumanie", "Serbie", "Croatie",
        "Bosnie-Herzégovine", "Albanie", "Grèce", "Turquie", "Arménie",
        "Géorgie", "Russie", "Ukraine", "Moldavie", "Belgique", "Pays-Bas",
        "Allemagne", "Suisse", "Autriche", "Hongrie", "République tchèque",
        "Slovaquie", "Bulgarie", "Macédoine du Nord", "Monténégro", "Kosovo"
    }

    asia = {
        "Vietnam", "Cambodge", "Laos", "Chine", "Japon", "Corée du Sud",
        "Philippines", "Thaïlande", "Indonésie", "Malaisie", "Inde",
        "Pakistan", "Bangladesh", "Sri Lanka", "Afghanistan", "Iran", "Irak"
    }

    result = {
        "is_dual_national": len(nationalities) > 1,
        "nationalities": nationalities,
        "diaspora_region": None,
        "diaspora_countries": [],
    }

    for nat in nationalities:
        if nat == "France":
            continue
        if nat in sub_saharan:
            result["diaspora_region"] = "Sub-Saharan Africa"
            result["diaspora_countries"].append(nat)
        elif nat in maghreb:
            result["diaspora_region"] = "Maghreb"
            result["diaspora_countries"].append(nat)
        elif nat in overseas or nat in {"Haïti"}:
            result["diaspora_region"] = "Caribbean/Overseas"
            result["diaspora_countries"].append(nat)
        elif nat in comoros:
            result["diaspora_region"] = "Comoros"
            result["diaspora_countries"].append(nat)
        elif nat in portugal:
            result["diaspora_region"] = "Portugal"
            result["diaspora_countries"].append(nat)
        elif nat in other_europe:
            result["diaspora_region"] = "Other Europe"
            result["diaspora_countries"].append(nat)
        elif nat in asia:
            result["diaspora_region"] = "Asia"
            result["diaspora_countries"].append(nat)

    return result


def analyze_dataset(players: list[dict]) -> dict:
    """Run comprehensive analysis on the dataset."""

    results = {
        "metadata": {
            "total_players": len(players),
            "analysis_date": datetime.now().isoformat(),
            "data_source": "Wikidata",
            "limitations": [
                "Missing Seine-Saint-Denis (93) - rate limited",
                "Missing Val-d'Oise (95) - rate limited",
                "Only includes players with Wikidata entries",
                "Birthplace != where player was raised/trained"
            ]
        },
        "demographics": {},
        "diaspora": {},
        "temporal": {},
        "geographic": {},
    }

    # Basic demographics
    nationalities_all = []
    dual_nationals = 0
    birth_years = []
    departments = defaultdict(int)
    diaspora_regions = defaultdict(int)
    diaspora_countries = defaultdict(int)

    enriched_players = []

    for player in players:
        # Extract data
        nats = player.get("nationalities", [])
        nationalities_all.extend(nats)

        if len(nats) > 1:
            dual_nationals += 1

        # Birth year
        dob = player.get("date_of_birth", "")
        if dob and len(dob) >= 4:
            try:
                year = int(dob[:4])
                birth_years.append(year)
            except ValueError:
                pass

        # Department
        birthplace = player.get("birthplace", {})
        bp_name = birthplace.get("name", "") if isinstance(birthplace, dict) else ""
        dept = extract_department_from_birthplace(bp_name)
        if dept:
            departments[dept] += 1

        # Diaspora categorization
        diaspora = categorize_diaspora(nats)
        if diaspora["diaspora_region"]:
            diaspora_regions[diaspora["diaspora_region"]] += 1
            for country in diaspora["diaspora_countries"]:
                diaspora_countries[country] += 1

        # Enrich player record
        enriched = {
            **player,
            "department": dept,
            "birth_year": int(dob[:4]) if dob and len(dob) >= 4 else None,
            "is_dual_national": diaspora["is_dual_national"],
            "diaspora_region": diaspora["diaspora_region"],
            "diaspora_countries": diaspora["diaspora_countries"],
        }
        enriched_players.append(enriched)

    # Compile results
    nat_counts = Counter(nationalities_all)

    results["demographics"] = {
        "total_players": len(players),
        "dual_nationals": dual_nationals,
        "dual_national_pct": round(100 * dual_nationals / len(players), 1),
        "top_nationalities": nat_counts.most_common(20),
    }

    results["diaspora"] = {
        "by_region": dict(diaspora_regions),
        "by_country": dict(Counter(diaspora_countries).most_common(20)),
        "total_diaspora": sum(diaspora_regions.values()),
        "diaspora_pct": round(100 * sum(diaspora_regions.values()) / len(players), 1),
    }

    # Temporal analysis
    year_counts = Counter(birth_years)
    decade_counts = defaultdict(int)
    for year, count in year_counts.items():
        decade = (year // 5) * 5
        decade_counts[decade] += count

    results["temporal"] = {
        "by_year": dict(sorted(year_counts.items())),
        "by_5year": dict(sorted(decade_counts.items())),
        "earliest_birth": min(birth_years) if birth_years else None,
        "latest_birth": max(birth_years) if birth_years else None,
    }

    # Geographic analysis
    dept_names = {
        "75": "Paris",
        "77": "Seine-et-Marne",
        "78": "Yvelines",
        "91": "Essonne",
        "92": "Hauts-de-Seine",
        "93": "Seine-Saint-Denis",
        "94": "Val-de-Marne",
        "95": "Val-d'Oise",
    }

    results["geographic"] = {
        "by_department": {
            dept: {"count": count, "name": dept_names.get(dept, dept)}
            for dept, count in sorted(departments.items(), key=lambda x: -x[1])
        },
        "missing_departments": ["93", "95"],
    }

    return results, enriched_players


def generate_article_stats(results: dict) -> str:
    """Generate statistics formatted for the Medium article."""

    output = []
    output.append("# Key Statistics for Article\n")
    output.append(f"*Generated: {results['metadata']['analysis_date']}*\n")

    output.append("\n## Headline Numbers\n")
    output.append(f"- **{results['demographics']['total_players']}** professional footballers born in Île-de-France (1980-2006)")
    output.append(f"- **{results['demographics']['dual_national_pct']}%** are dual nationals")
    output.append(f"- **{results['diaspora']['diaspora_pct']}%** have African diaspora background")

    output.append("\n## Diaspora Breakdown\n")
    output.append("| Region | Players | % of Total |")
    output.append("|--------|---------|------------|")
    total = results['demographics']['total_players']
    for region, count in sorted(results['diaspora']['by_region'].items(), key=lambda x: -x[1]):
        pct = round(100 * count / total, 1)
        output.append(f"| {region} | {count} | {pct}% |")

    output.append("\n## Top Countries (besides France)\n")
    output.append("| Country | Players |")
    output.append("|---------|---------|")
    for country, count in list(results['diaspora']['by_country'].items())[:10]:
        output.append(f"| {country} | {count} |")

    output.append("\n## By Département\n")
    output.append("| Département | Players |")
    output.append("|-------------|---------|")
    for dept, info in results['geographic']['by_department'].items():
        output.append(f"| {info['name']} ({dept}) | {info['count']} |")
    output.append("| Seine-Saint-Denis (93) | ⚠️ Data missing |")
    output.append("| Val-d'Oise (95) | ⚠️ Data missing |")

    output.append("\n## Birth Year Trends\n")
    output.append("| Period | Players |")
    output.append("|--------|---------|")
    for period, count in sorted(results['temporal']['by_5year'].items()):
        output.append(f"| {period}-{period+4} | {count} |")

    output.append("\n## Limitations\n")
    for limitation in results['metadata']['limitations']:
        output.append(f"- {limitation}")

    return "\n".join(output)


def create_huggingface_dataset(enriched_players: list[dict], output_dir: Path):
    """Create dataset in Hugging Face format."""

    # Convert to DataFrame
    df = pd.DataFrame(enriched_players)

    # Select and rename columns for HF
    hf_columns = {
        "wikidata_id": "wikidata_id",
        "name": "name",
        "date_of_birth": "birth_date",
        "birth_year": "birth_year",
        "department": "birth_department",
        "nationalities": "nationalities",
        "is_dual_national": "is_dual_national",
        "diaspora_region": "diaspora_region",
        "diaspora_countries": "diaspora_countries",
    }

    # Filter columns that exist
    available_cols = [c for c in hf_columns.keys() if c in df.columns]
    df_hf = df[available_cols].rename(columns={k: v for k, v in hf_columns.items() if k in available_cols})

    # Add birthplace name
    df_hf["birth_city"] = df.apply(
        lambda x: x.get("birthplace", {}).get("name", "") if isinstance(x.get("birthplace"), dict) else "",
        axis=1
    )

    # Save in multiple formats
    output_dir.mkdir(parents=True, exist_ok=True)

    # CSV
    df_hf.to_csv(output_dir / "idf_footballers.csv", index=False)

    # Parquet (more efficient)
    df_hf.to_parquet(output_dir / "idf_footballers.parquet", index=False)

    # JSON Lines (HF preferred format)
    df_hf.to_json(output_dir / "idf_footballers.jsonl", orient="records", lines=True, force_ascii=False)

    print(f"Saved {len(df_hf)} records to {output_dir}")

    return df_hf


def main():
    """Run full analysis pipeline."""

    # Paths
    project_root = Path(__file__).parent.parent.parent
    raw_data = project_root / "data" / "raw" / "wikidata" / "idf_footballers.json"
    processed_dir = project_root / "data" / "processed"
    hf_dir = project_root / "data" / "huggingface"

    print("=" * 60)
    print("IDF Footballers Analysis")
    print("=" * 60)

    # Load data
    print("\n1. Loading data...")
    players = load_data(raw_data)
    print(f"   Loaded {len(players)} players")

    # Analyze
    print("\n2. Running analysis...")
    results, enriched_players = analyze_dataset(players)

    # Save analysis results
    print("\n3. Saving results...")
    processed_dir.mkdir(parents=True, exist_ok=True)

    with open(processed_dir / "analysis_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    # Generate article stats
    article_stats = generate_article_stats(results)
    with open(processed_dir / "article_stats.md", "w") as f:
        f.write(article_stats)
    print(f"   Saved article stats to {processed_dir / 'article_stats.md'}")

    # Create HF dataset
    print("\n4. Creating Hugging Face dataset...")
    df_hf = create_huggingface_dataset(enriched_players, hf_dir)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTotal players: {results['demographics']['total_players']}")
    print(f"Dual nationals: {results['demographics']['dual_nationals']} ({results['demographics']['dual_national_pct']}%)")
    print(f"African diaspora: {results['diaspora']['total_diaspora']} ({results['diaspora']['diaspora_pct']}%)")

    print("\nDiaspora by region:")
    for region, count in sorted(results['diaspora']['by_region'].items(), key=lambda x: -x[1]):
        print(f"  {region}: {count}")

    print("\nTop countries:")
    for country, count in list(results['diaspora']['by_country'].items())[:5]:
        print(f"  {country}: {count}")

    print("\n" + "=" * 60)
    print("FILES CREATED")
    print("=" * 60)
    print(f"  {processed_dir / 'analysis_results.json'}")
    print(f"  {processed_dir / 'article_stats.md'}")
    print(f"  {hf_dir / 'idf_footballers.csv'}")
    print(f"  {hf_dir / 'idf_footballers.parquet'}")
    print(f"  {hf_dir / 'idf_footballers.jsonl'}")


if __name__ == "__main__":
    main()
