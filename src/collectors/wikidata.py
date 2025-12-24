"""
Wikidata collector for football players born in Île-de-France.

Wikidata is our primary source for birthplace data because:
- It's free and legal to query
- It has structured geographic data
- It allows SPARQL queries

Usage:
    python src/collectors/wikidata.py
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from loguru import logger


class WikidataCollector:
    """Collector for football player data from Wikidata."""

    ENDPOINT = "https://query.wikidata.org/sparql"

    # Île-de-France Wikidata ID
    IDF_QID = "Q13917"

    # Département QIDs for more precise queries (verified from Wikidata)
    DEPARTMENTS = {
        "75": "Q90",        # Paris
        "77": "Q12753",     # Seine-et-Marne
        "78": "Q12820",     # Yvelines
        "91": "Q12549",     # Essonne
        "92": "Q12543",     # Hauts-de-Seine
        "93": "Q12761",     # Seine-Saint-Denis
        "94": "Q12788",     # Val-de-Marne
        "95": "Q12784",     # Val-d'Oise
    }

    def __init__(self, output_dir: Path = Path("data/raw/wikidata")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._client = httpx.Client(
            headers={
                # Wikidata requires a proper User-Agent with contact info
                "User-Agent": "PSG-Diaspora-Dataset/1.0 (https://github.com/ldiaby/psg-diaspora-dataset; research project) Python/httpx",
                "Accept": "application/sparql-results+json",
            },
            timeout=120.0,
        )

    def query(self, sparql: str) -> list[dict[str, Any]]:
        """Execute a SPARQL query against Wikidata."""
        logger.info("Executing SPARQL query...")

        response = self._client.get(
            self.ENDPOINT,
            params={"query": sparql, "format": "json"},
        )
        response.raise_for_status()

        data = response.json()
        results = data.get("results", {}).get("bindings", [])

        logger.info(f"Query returned {len(results)} results")
        return results

    def get_idf_footballers(
        self,
        birth_year_start: int = 1980,
        birth_year_end: int = 2006,
    ) -> list[dict[str, Any]]:
        """
        Get all football players born in Île-de-France within date range.

        Returns structured player data with birthplace, nationality, etc.
        """
        sparql = f"""
        SELECT DISTINCT
            ?player
            ?playerLabel
            ?playerDescription
            ?birthDate
            ?birthPlace
            ?birthPlaceLabel
            ?birthPlaceCoord
            (GROUP_CONCAT(DISTINCT ?nationalityLabel; separator=", ") AS ?nationalities)
            ?image
        WHERE {{
            # Is a football player (association football player)
            ?player wdt:P106 wd:Q937857 .

            # Has birthplace in Île-de-France (recursive through administrative divisions)
            ?player wdt:P19 ?birthPlace .
            ?birthPlace wdt:P131* wd:{self.IDF_QID} .

            # Has birth date in range
            ?player wdt:P569 ?birthDate .
            FILTER(YEAR(?birthDate) >= {birth_year_start} && YEAR(?birthDate) <= {birth_year_end})

            # Optional: nationality
            OPTIONAL {{
                ?player wdt:P27 ?nationality .
                ?nationality rdfs:label ?nationalityLabel .
                FILTER(LANG(?nationalityLabel) = "fr")
            }}

            # Optional: coordinates of birthplace
            OPTIONAL {{ ?birthPlace wdt:P625 ?birthPlaceCoord }}

            # Optional: image
            OPTIONAL {{ ?player wdt:P18 ?image }}

            SERVICE wikibase:label {{
                bd:serviceParam wikibase:language "fr,en" .
            }}
        }}
        GROUP BY ?player ?playerLabel ?playerDescription ?birthDate ?birthPlace ?birthPlaceLabel ?birthPlaceCoord ?image
        ORDER BY ?birthDate
        """

        results = self.query(sparql)
        return self._parse_results(results)

    def get_footballers_by_department(self, dept_code: str) -> list[dict[str, Any]]:
        """Get footballers born in a specific département."""
        dept_qid = self.DEPARTMENTS.get(dept_code)
        if not dept_qid:
            raise ValueError(f"Unknown département: {dept_code}")

        # Simplified query - limit depth of P131 to avoid timeout
        sparql = f"""
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

            # Birthplace is in département (up to 3 levels: commune -> arrondissement -> dept)
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

        results = self.query(sparql)
        return self._parse_results(results)

    def get_player_details(self, player_qid: str) -> dict[str, Any]:
        """Get detailed information about a specific player."""
        sparql = f"""
        SELECT
            ?player
            ?playerLabel
            ?playerDescription
            ?birthDate
            ?birthPlace
            ?birthPlaceLabel
            ?birthPlaceCoord
            ?height
            ?position
            ?positionLabel
            (GROUP_CONCAT(DISTINCT ?teamLabel; separator=", ") AS ?teams)
            (GROUP_CONCAT(DISTINCT ?nationalityLabel; separator=", ") AS ?nationalities)
        WHERE {{
            BIND(wd:{player_qid} AS ?player)

            OPTIONAL {{ ?player wdt:P569 ?birthDate }}
            OPTIONAL {{
                ?player wdt:P19 ?birthPlace .
                OPTIONAL {{ ?birthPlace wdt:P625 ?birthPlaceCoord }}
            }}
            OPTIONAL {{ ?player wdt:P2048 ?height }}
            OPTIONAL {{ ?player wdt:P413 ?position }}
            OPTIONAL {{ ?player wdt:P54 ?team }}
            OPTIONAL {{ ?player wdt:P27 ?nationality }}

            SERVICE wikibase:label {{
                bd:serviceParam wikibase:language "fr,en" .
                ?player rdfs:label ?playerLabel .
                ?player schema:description ?playerDescription .
                ?birthPlace rdfs:label ?birthPlaceLabel .
                ?position rdfs:label ?positionLabel .
                ?team rdfs:label ?teamLabel .
                ?nationality rdfs:label ?nationalityLabel .
            }}
        }}
        GROUP BY ?player ?playerLabel ?playerDescription ?birthDate ?birthPlace ?birthPlaceLabel ?birthPlaceCoord ?height ?position ?positionLabel
        """

        results = self.query(sparql)
        if results:
            return self._parse_results(results)[0]
        return {}

    def _parse_results(self, results: list[dict]) -> list[dict[str, Any]]:
        """Parse SPARQL results into clean dictionaries."""
        parsed = []

        for row in results:
            player = {
                "wikidata_id": self._extract_qid(row.get("player", {})),
                "name": row.get("playerLabel", {}).get("value", ""),
                "description": row.get("playerDescription", {}).get("value", ""),
                "date_of_birth": self._parse_date(row.get("birthDate", {})),
                "birthplace": {
                    "name": row.get("birthPlaceLabel", {}).get("value", ""),
                    "wikidata_id": self._extract_qid(row.get("birthPlace", {})),
                    "coordinates": self._parse_coordinates(row.get("birthPlaceCoord", {})),
                },
                "nationalities": self._parse_list(row.get("nationalities", {})),
                "image_url": row.get("image", {}).get("value", ""),
            }
            parsed.append(player)

        return parsed

    def _extract_qid(self, value: dict) -> str | None:
        """Extract QID from Wikidata URI."""
        uri = value.get("value", "")
        if "/entity/Q" in uri:
            return uri.split("/")[-1]
        return None

    def _parse_date(self, value: dict) -> str | None:
        """Parse date from Wikidata format."""
        date_str = value.get("value", "")
        if date_str:
            # Wikidata dates are in ISO format, sometimes with time
            return date_str.split("T")[0]
        return None

    def _parse_coordinates(self, value: dict) -> dict | None:
        """Parse coordinates from Wikidata point format."""
        coord_str = value.get("value", "")
        if coord_str and coord_str.startswith("Point("):
            # Format: "Point(longitude latitude)"
            coords = coord_str[6:-1].split()
            if len(coords) == 2:
                return {
                    "longitude": float(coords[0]),
                    "latitude": float(coords[1]),
                }
        return None

    def _parse_list(self, value: dict) -> list[str]:
        """Parse comma-separated list from Wikidata."""
        list_str = value.get("value", "")
        if list_str:
            return [item.strip() for item in list_str.split(",") if item.strip()]
        return []

    def save(self, data: list[dict], filename: str) -> Path:
        """Save collected data to JSON file."""
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "metadata": {
                        "source": "wikidata",
                        "collected_at": datetime.now().isoformat(),
                        "count": len(data),
                    },
                    "players": data,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        logger.info(f"Saved {len(data)} players to {filepath}")
        return filepath

    def close(self):
        """Close HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Main collection script."""
    import sys

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    with WikidataCollector() as collector:
        all_players = []

        # Collect by département to avoid timeout
        # The recursive IDF query is too expensive
        logger.info("Collecting footballers by département (1980-2006)...")

        for dept_code, dept_name in [
            ("75", "Paris"),
            ("92", "Hauts-de-Seine"),
            ("93", "Seine-Saint-Denis"),
            ("94", "Val-de-Marne"),
            ("95", "Val-d'Oise"),
            ("77", "Seine-et-Marne"),
            ("78", "Yvelines"),
            ("91", "Essonne"),
        ]:
            logger.info(f"Querying {dept_name} ({dept_code})...")
            try:
                players = collector.get_footballers_by_department(dept_code)
                logger.info(f"  Found {len(players)} players in {dept_name}")
                all_players.extend(players)
            except Exception as e:
                logger.error(f"  Failed for {dept_name}: {e}")

            # Small delay between queries
            import time
            time.sleep(2)

        # Deduplicate by wikidata_id
        seen_ids = set()
        unique_players = []
        for p in all_players:
            if p['wikidata_id'] and p['wikidata_id'] not in seen_ids:
                seen_ids.add(p['wikidata_id'])
                unique_players.append(p)

        # Save results
        output_file = collector.save(unique_players, "idf_footballers.json")

        # Print summary
        print(f"\n{'='*60}")
        print(f"Collection complete!")
        print(f"{'='*60}")
        print(f"Total players found: {len(unique_players)}")
        print(f"Output file: {output_file}")

        # Show sample
        if unique_players:
            print(f"\nSample players:")
            for p in unique_players[:10]:
                print(f"  - {p['name']} ({p['date_of_birth']}) - {p['birthplace']['name']}")
                if p.get('nationalities'):
                    print(f"    Nationalities: {', '.join(p['nationalities'])}")


if __name__ == "__main__":
    main()
