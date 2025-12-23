"""
Data schemas for PSG Diaspora Dataset

Defines the structure of our main datasets with clear definitions
to avoid ambiguity in what constitutes a "Francilien" player.
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class PlayerOriginType(Enum):
    """
    How a player is connected to Île-de-France.
    A player can have multiple origin types.
    """
    BORN = "born"                    # Born in Île-de-France
    TRAINED = "trained"              # Trained at a club in Île-de-France (any level)
    PSG_ACADEMY = "psg_academy"      # Specifically trained at PSG academy
    RAISED = "raised"                # Grew up in Île-de-France (even if born elsewhere)


class CareerStatus(Enum):
    """Current career status of the player."""
    ACTIVE = "active"
    RETIRED = "retired"
    YOUTH = "youth"          # Still in academy
    UNKNOWN = "unknown"


@dataclass
class Location:
    """Geographic location with coordinates."""
    city: str
    department: Optional[str] = None        # French département code (75, 93, etc.)
    region: Optional[str] = None            # Region name
    country: str = "France"
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class ClubSpell:
    """A period spent at a club."""
    club_name: str
    club_country: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_loan: bool = False
    is_youth: bool = False                  # Youth/academy or senior team
    appearances: Optional[int] = None
    goals: Optional[int] = None


@dataclass
class InternationalCareer:
    """International career information."""
    country: str
    level: str                              # "senior", "U21", "U19", etc.
    caps: int = 0
    goals: int = 0
    debut_date: Optional[date] = None


@dataclass
class Player:
    """
    Main player entity.

    Key distinction: We track BOTH birthplace AND training location
    to properly analyze the relationship between origin and football development.
    """
    # Identifiers
    player_id: str                          # Internal unique ID
    transfermarkt_id: Optional[str] = None
    fbref_id: Optional[str] = None
    wikidata_id: Optional[str] = None

    # Basic info
    name: str = ""
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: list[str] = field(default_factory=list)  # Can have multiple

    # Geographic origins - CRITICAL for analysis
    birthplace: Optional[Location] = None
    training_locations: list[Location] = field(default_factory=list)  # Where trained as youth

    # Origin classification
    origin_types: list[PlayerOriginType] = field(default_factory=list)

    # Physical attributes
    height_cm: Optional[int] = None
    position: Optional[str] = None
    preferred_foot: Optional[str] = None

    # Career
    status: CareerStatus = CareerStatus.UNKNOWN
    club_history: list[ClubSpell] = field(default_factory=list)
    current_club: Optional[str] = None
    market_value_eur: Optional[int] = None

    # International
    international_career: list[InternationalCareer] = field(default_factory=list)

    # PSG-specific
    psg_academy_years: Optional[tuple[int, int]] = None  # (start_year, end_year)
    reached_psg_first_team: bool = False
    psg_first_team_appearances: int = 0

    # Metadata
    data_sources: list[str] = field(default_factory=list)
    last_updated: Optional[date] = None
    data_quality_score: float = 0.0  # 0-1, based on completeness


@dataclass
class Club:
    """Football club entity."""
    club_id: str
    name: str
    location: Location
    founded_year: Optional[int] = None
    current_league: Optional[str] = None
    is_professional: bool = False
    has_academy: bool = False

    # For French clubs
    fff_id: Optional[str] = None


@dataclass
class DemographicData:
    """
    Demographic data for a geographic unit (département, commune).
    Used to correlate with football talent production.
    """
    geo_code: str                           # INSEE code
    geo_name: str
    year: int

    # Population
    total_population: int
    population_under_20: Optional[int] = None
    population_density: Optional[float] = None  # per km²

    # Migration data
    immigrant_population: Optional[int] = None
    immigrant_share: Optional[float] = None     # percentage

    # By origin (if available)
    origin_maghreb: Optional[int] = None
    origin_subsaharan_africa: Optional[int] = None
    origin_europe: Optional[int] = None
    origin_asia: Optional[int] = None
    origin_other: Optional[int] = None

    # Socioeconomic
    median_income: Optional[float] = None
    unemployment_rate: Optional[float] = None
    poverty_rate: Optional[float] = None


@dataclass
class FootballInfrastructure:
    """Football infrastructure in a geographic area."""
    geo_code: str
    geo_name: str

    # Clubs
    num_clubs: int = 0
    num_professional_clubs: int = 0
    num_licensed_players: Optional[int] = None

    # Facilities
    num_stadiums: int = 0
    num_city_stades: int = 0
    num_training_grounds: int = 0


@dataclass
class MediaArticle:
    """Article from media corpus for NLP analysis."""
    article_id: str
    source: str                             # "lequipe", "leparisien", "sofoot"
    url: Optional[str] = None
    title: str = ""
    content: str = ""
    publication_date: Optional[date] = None
    author: Optional[str] = None

    # Extracted entities
    players_mentioned: list[str] = field(default_factory=list)
    clubs_mentioned: list[str] = field(default_factory=list)
    locations_mentioned: list[str] = field(default_factory=list)

    # NLP analysis results (to be filled later)
    sentiment_score: Optional[float] = None
    topics: list[str] = field(default_factory=list)
    quartier_mentions: int = 0
    diversity_mentions: int = 0
