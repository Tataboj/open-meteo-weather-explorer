"""Supported historical weather variables and API endpoints."""

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

HOURLY_VARIABLES = (
    "temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m",
)
DAILY_VARIABLES = (
    "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max",
)
