#!/usr/bin/env python3
"""
Retry script for collecting Seine-Saint-Denis (93) and Val-d'Oise (95) data.

Run this after the Wikidata rate limit has reset (typically 1 hour).

Usage:
    ./venv/bin/python scripts/retry_93_95.py
"""

import json
import time
from datetime import datetime
from pathlib import Path

import httpx


def check_rate_limit():
    """Check if Wikidata rate limit has reset."""
    test_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 1"

    client = httpx.Client(
        headers={
            "User-Agent": "PSG-Diaspora-Dataset/1.0 (research project)",
            "Accept": "application/sparql-results+json",
        },
        timeout=30
    )

    try:
        response = client.get(
            "https://query.wikidata.org/sparql",
            params={"query": test_query, "format": "json"}
        )
        return response.status_code == 200
    except Exception:
        return False
    finally:
        client.close()


def query_department(dept_qid: str, dept_name: str, client: httpx.Client) -> list:
    """Query footballers from a specific département."""

    query = f"""
    SELECT DISTINCT
        ?player
        ?playerLabel
        ?birthDate
        ?birthPlace
        ?birthPlaceLabel
        (GROUP_CONCAT(DISTINCT ?nationalityLabel; separator=", ") AS ?nationalities)
    WHERE {{
        ?player wdt:P106 wd:Q937857 .
        ?player wdt:P19 ?birthPlace .

        {{
            ?birthPlace wdt:P131 wd:{dept_qid} .
        }} UNION {{
            ?birthPlace wdt:P131/wdt:P131 wd:{dept_qid} .
        }} UNION {{
            ?birthPlace wdt:P131/wdt:P131/wdt:P131 wd:{dept_qid} .
        }}

        ?player wdt:P569 ?birthDate .
        FILTER(YEAR(?birthDate) >= 1980 && YEAR(?birthDate) <= 2006)

        OPTIONAL {{
            ?player wdt:P27 ?nationality .
            ?nationality rdfs:label ?nationalityLabel .
            FILTER(LANG(?nationalityLabel) = "fr")
        }}

        SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "fr,en" .
        }}
    }}
    GROUP BY ?player ?playerLabel ?birthDate ?birthPlace ?birthPlaceLabel
    ORDER BY ?birthDate
    """

    print(f"  Querying {dept_name}...")

    try:
        response = client.get(
            "https://query.wikidata.org/sparql",
            params={"query": query, "format": "json"}
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", {}).get("bindings", [])
            print(f"    Found {len(results)} players")
            return results
        else:
            print(f"    HTTP {response.status_code}")
            return []

    except Exception as e:
        print(f"    Error: {e}")
        return []


def parse_results(results: list) -> list:
    """Parse SPARQL results into player dicts."""
    players = []

    for row in results:
        player = {
            "wikidata_id": row.get("player", {}).get("value", "").split("/")[-1],
            "name": row.get("playerLabel", {}).get("value", ""),
            "date_of_birth": row.get("birthDate", {}).get("value", "").split("T")[0],
            "birthplace": {
                "name": row.get("birthPlaceLabel", {}).get("value", ""),
                "wikidata_id": row.get("birthPlace", {}).get("value", "").split("/")[-1],
            },
            "nationalities": [
                n.strip()
                for n in row.get("nationalities", {}).get("value", "").split(",")
                if n.strip()
            ],
        }
        players.append(player)

    return players


def main():
    print("=" * 60)
    print("Retry Collection: Seine-Saint-Denis (93) & Val-d'Oise (95)")
    print("=" * 60)

    # Check rate limit
    print("\n1. Checking rate limit...")
    if not check_rate_limit():
        print("   Rate limit still active. Try again later.")
        return

    print("   Rate limit cleared!")

    # Départements to collect
    departments = [
        ("Q12761", "Seine-Saint-Denis (93)", "93"),
        ("Q12784", "Val-d'Oise (95)", "95"),
    ]

    # Create client
    client = httpx.Client(
        headers={
            "User-Agent": "PSG-Diaspora-Dataset/1.0 (research project)",
            "Accept": "application/sparql-results+json",
        },
        timeout=120
    )

    all_players = []

    print("\n2. Collecting data...")
    for dept_qid, dept_name, dept_code in departments:
        results = query_department(dept_qid, dept_name, client)
        players = parse_results(results)

        # Add department code
        for p in players:
            p["department"] = dept_code

        all_players.extend(players)
        time.sleep(3)  # Be nice

    client.close()

    # Save results
    output_dir = Path(__file__).parent.parent / "data" / "raw" / "wikidata"
    output_file = output_dir / "idf_footballers_93_95.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "collected_at": datetime.now().isoformat(),
                "departments": ["93", "95"],
                "count": len(all_players),
            },
            "players": all_players,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n3. Saved {len(all_players)} players to {output_file}")

    # Merge with main dataset
    print("\n4. Merging with main dataset...")

    main_file = output_dir / "idf_footballers.json"
    with open(main_file) as f:
        main_data = json.load(f)

    # Get existing IDs
    existing_ids = {p["wikidata_id"] for p in main_data["players"]}

    # Add new players
    new_count = 0
    for player in all_players:
        if player["wikidata_id"] not in existing_ids:
            main_data["players"].append(player)
            existing_ids.add(player["wikidata_id"])
            new_count += 1

    # Update metadata
    main_data["metadata"]["count"] = len(main_data["players"])
    main_data["metadata"]["last_updated"] = datetime.now().isoformat()
    main_data["metadata"]["includes_93_95"] = True

    # Save merged
    with open(main_file, "w", encoding="utf-8") as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)

    print(f"   Added {new_count} new players")
    print(f"   Total players now: {len(main_data['players'])}")

    print("\n5. Re-running analysis...")
    import subprocess
    subprocess.run(["./venv/bin/python", "src/analysis/analyze_players.py"])

    print("\n" + "=" * 60)
    print("DONE! 93/95 data collected and merged.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Review data/processed/article_stats.md")
    print("  2. Re-generate charts: ./venv/bin/python src/visualization/charts.py")
    print("  3. Commit changes: git add -A && git commit -m 'Add 93/95 data'")


if __name__ == "__main__":
    main()
