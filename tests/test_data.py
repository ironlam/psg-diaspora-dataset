"""
Basic tests for the dataset.
"""

import json
from pathlib import Path

import pytest


DATA_DIR = Path(__file__).parent.parent / "data"


def test_raw_data_exists():
    """Test that raw data file exists."""
    filepath = DATA_DIR / "raw" / "wikidata" / "idf_footballers.json"
    assert filepath.exists(), f"Raw data not found at {filepath}"


def test_raw_data_structure():
    """Test that raw data has expected structure."""
    filepath = DATA_DIR / "raw" / "wikidata" / "idf_footballers.json"
    with open(filepath) as f:
        data = json.load(f)

    assert "players" in data or isinstance(data, list), "Data should have 'players' key or be a list"

    players = data.get("players", data)
    assert len(players) > 0, "Should have at least one player"

    # Check first player has expected fields
    player = players[0]
    expected_fields = ["wikidata_id", "name", "date_of_birth"]
    for field in expected_fields:
        assert field in player, f"Player should have '{field}' field"


def test_processed_data_exists():
    """Test that processed data exists."""
    filepath = DATA_DIR / "processed" / "analysis_results.json"
    assert filepath.exists(), f"Processed data not found at {filepath}"


def test_analysis_results_structure():
    """Test that analysis results have expected structure."""
    filepath = DATA_DIR / "processed" / "analysis_results.json"
    with open(filepath) as f:
        data = json.load(f)

    expected_keys = ["metadata", "demographics", "diaspora", "temporal", "geographic"]
    for key in expected_keys:
        assert key in data, f"Analysis should have '{key}' key"


def test_huggingface_data_exists():
    """Test that HuggingFace data exists."""
    hf_dir = DATA_DIR / "huggingface"

    expected_files = [
        "idf_footballers.csv",
        "idf_footballers.parquet",
        "idf_footballers.jsonl",
        "README.md",
    ]

    for filename in expected_files:
        filepath = hf_dir / filename
        assert filepath.exists(), f"HuggingFace file not found: {filepath}"


def test_player_count():
    """Test that we have a reasonable number of players."""
    filepath = DATA_DIR / "raw" / "wikidata" / "idf_footballers.json"
    with open(filepath) as f:
        data = json.load(f)

    players = data.get("players", data)

    # Should have at least 500 players (we have 713)
    assert len(players) >= 500, f"Expected at least 500 players, got {len(players)}"


def test_dual_nationality_percentage():
    """Test that dual nationality percentage is reasonable."""
    filepath = DATA_DIR / "processed" / "analysis_results.json"
    with open(filepath) as f:
        data = json.load(f)

    pct = data["demographics"]["dual_national_pct"]

    # Should be between 20% and 60%
    assert 20 <= pct <= 60, f"Dual national percentage {pct}% seems unreasonable"


def test_diaspora_regions():
    """Test that diaspora regions are as expected."""
    filepath = DATA_DIR / "processed" / "analysis_results.json"
    with open(filepath) as f:
        data = json.load(f)

    regions = data["diaspora"]["by_region"]

    # Should have Sub-Saharan Africa and Maghreb
    assert "Sub-Saharan Africa" in regions, "Should have Sub-Saharan Africa region"
    assert "Maghreb" in regions, "Should have Maghreb region"

    # Sub-Saharan should be largest
    assert regions["Sub-Saharan Africa"] >= regions["Maghreb"], \
        "Sub-Saharan Africa should have more players than Maghreb"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
