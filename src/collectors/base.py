"""
Base collector class for data sources.
"""

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import httpx
from loguru import logger


class BaseCollector(ABC):
    """Base class for all data collectors."""

    def __init__(
        self,
        base_url: str,
        rate_limit: float = 2.0,
        output_dir: Path = Path("data/raw"),
    ):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._last_request_time = 0.0
        self._client = httpx.Client(
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; research project)",
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            },
            timeout=30.0,
            follow_redirects=True,
        )

    def _wait_for_rate_limit(self) -> None:
        """Ensure we respect the rate limit between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)

    def get(self, url: str) -> httpx.Response:
        """Make a GET request with rate limiting."""
        self._wait_for_rate_limit()
        logger.info(f"Fetching: {url}")

        response = self._client.get(url)
        self._last_request_time = time.time()

        response.raise_for_status()
        return response

    @abstractmethod
    def collect(self, **kwargs) -> list[dict[str, Any]]:
        """Collect data from the source. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def parse(self, response: httpx.Response) -> dict[str, Any]:
        """Parse response into structured data. Must be implemented by subclasses."""
        pass

    def save(self, data: list[dict], filename: str) -> Path:
        """Save collected data to JSON file."""
        import json

        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

        logger.info(f"Saved {len(data)} records to {filepath}")
        return filepath

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
