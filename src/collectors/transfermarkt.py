"""
Transfermarkt data collector.

Collects player data from Transfermarkt, focusing on:
- PSG academy players
- Players born in Île-de-France
- Players trained at Île-de-France clubs

NOTE: Transfermarkt has strict scraping policies. Consider using:
- Their official API (if available)
- Cached datasets from Kaggle
- The `soccerdata` Python package
"""

from pathlib import Path
from typing import Any
from bs4 import BeautifulSoup
from loguru import logger

from .base import BaseCollector


class TransfermarktCollector(BaseCollector):
    """Collector for Transfermarkt player data."""

    def __init__(self, output_dir: Path = Path("data/raw/transfermarkt")):
        super().__init__(
            base_url="https://www.transfermarkt.com",
            rate_limit=3.0,  # Be respectful
            output_dir=output_dir,
        )

        # PSG club ID on Transfermarkt
        self.psg_id = "583"

        # Île-de-France clubs to track (add more as needed)
        self.idf_clubs = {
            "psg": "583",
            "paris_fc": "1969",
            "red_star": "1078",
            "creteil": "2185",
            # Add more clubs...
        }

    def get_psg_academy_players(self, season: str = "2024") -> list[dict]:
        """
        Get list of players from PSG academy.

        Args:
            season: Season year (e.g., "2024" for 2024/25)

        Returns:
            List of player dicts with basic info
        """
        # URL pattern for youth squad
        url = f"{self.base_url}/paris-saint-germain/startseite/verein/{self.psg_id}/saison_id/{season}/plus/1"

        try:
            response = self.get(url)
            return self._parse_squad_page(response.text)
        except Exception as e:
            logger.error(f"Failed to fetch PSG academy: {e}")
            return []

    def get_player_details(self, player_id: str) -> dict[str, Any]:
        """
        Get detailed information about a player.

        Args:
            player_id: Transfermarkt player ID

        Returns:
            Dict with player details
        """
        url = f"{self.base_url}/spieler/profil/spieler/{player_id}"

        try:
            response = self.get(url)
            return self._parse_player_page(response.text)
        except Exception as e:
            logger.error(f"Failed to fetch player {player_id}: {e}")
            return {}

    def _parse_squad_page(self, html: str) -> list[dict]:
        """Parse squad listing page."""
        soup = BeautifulSoup(html, "lxml")
        players = []

        # Find player rows in the squad table
        # NOTE: Transfermarkt HTML structure may change
        table = soup.find("table", class_="items")
        if not table:
            logger.warning("Could not find squad table")
            return []

        for row in table.find_all("tr", class_=["odd", "even"]):
            try:
                player = self._parse_player_row(row)
                if player:
                    players.append(player)
            except Exception as e:
                logger.warning(f"Failed to parse row: {e}")

        return players

    def _parse_player_row(self, row) -> dict[str, Any] | None:
        """Parse a single player row from squad table."""
        # Extract player link and ID
        link = row.find("a", class_="spielprofil_tooltip")
        if not link:
            return None

        href = link.get("href", "")
        player_id = href.split("/")[-1] if "/" in href else None

        name = link.get_text(strip=True)

        # Extract position
        position_cell = row.find("td", class_="posrela")
        position = position_cell.get_text(strip=True) if position_cell else None

        # Extract age/DOB
        age_cell = row.find("td", class_="zentriert")
        age = age_cell.get_text(strip=True) if age_cell else None

        return {
            "transfermarkt_id": player_id,
            "name": name,
            "position": position,
            "age": age,
            "source_url": f"{self.base_url}{href}" if href else None,
        }

    def _parse_player_page(self, html: str) -> dict[str, Any]:
        """Parse individual player profile page."""
        soup = BeautifulSoup(html, "lxml")

        data = {}

        # Player name
        header = soup.find("h1", class_="data-header__headline-wrapper")
        if header:
            data["name"] = header.get_text(strip=True)

        # Info box contains key details
        info_table = soup.find("div", class_="info-table")
        if info_table:
            for row in info_table.find_all("span", class_="info-table__content"):
                label = row.find_previous("span", class_="info-table__content--regular")
                if label:
                    key = label.get_text(strip=True).lower().replace(":", "")
                    value = row.get_text(strip=True)
                    data[key] = value

        # Career history
        data["career_history"] = self._parse_career_history(soup)

        return data

    def _parse_career_history(self, soup) -> list[dict]:
        """Parse player's career history."""
        history = []

        # Find career table
        career_table = soup.find("div", class_="grid tm-player-transfer-history-grid")
        if not career_table:
            return history

        # Parse each transfer/spell
        # Implementation depends on current Transfermarkt structure

        return history

    def collect(self, **kwargs) -> list[dict[str, Any]]:
        """
        Main collection method.

        Collects:
        1. PSG academy players
        2. Player details for each
        """
        players = []

        # Get PSG academy roster
        academy_players = self.get_psg_academy_players()
        logger.info(f"Found {len(academy_players)} PSG academy players")

        # Get details for each player
        for player in academy_players:
            if player.get("transfermarkt_id"):
                details = self.get_player_details(player["transfermarkt_id"])
                player.update(details)
                players.append(player)

        return players

    def parse(self, response) -> dict[str, Any]:
        """Generic parse method - delegates to specific parsers."""
        return self._parse_player_page(response.text)


if __name__ == "__main__":
    # Example usage
    from loguru import logger
    import sys

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    with TransfermarktCollector() as collector:
        # Collect PSG academy data
        data = collector.collect()
        collector.save(data, "psg_academy_players.json")
