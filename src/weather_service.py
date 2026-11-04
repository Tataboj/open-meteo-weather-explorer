"""External Open-Meteo API access, isolated from Streamlit widgets."""

from datetime import date, timedelta
from typing import Any

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from .config import ARCHIVE_URL, GEOCODING_URL
from .data_processing import daily_index, hourly_index, trim_hourly_to_local_dates
from .location_matching import normalize_search_query


class WeatherDataService:
    @staticmethod
    def _session():
        return retry(requests_cache.CachedSession(".cache/openmeteo", expire_after=3600), retries=3, backoff_factor=0.3)

    @staticmethod
    def get_coordinates(name: str) -> list[dict[str, Any]]:
        response = WeatherDataService._session().get(
            GEOCODING_URL, params={"name": normalize_search_query(name), "count": 100, "language": "en", "format": "json"}, timeout=20,
        )
        response.raise_for_status()
        return response.json().get("results", [])

    @staticmethod
    def fetch_historical_data(
        lat: float, lon: float, start_date: date, end_date: date,
        variables: list[str], granularity: str, timezone: str,
    ) -> pd.DataFrame:
        if granularity not in {"hourly", "daily"}:
            raise ValueError("Unsupported granularity")
        session = WeatherDataService._session()
        client = openmeteo_requests.Client(session=session)
        api_timezone = "UTC" if granularity == "hourly" else timezone
        # Hourly requests use UTC timestamps, but the user chooses local dates.
        # Ask for padding days to include both local midnight boundaries.
        api_start = start_date - timedelta(days=1) if granularity == "hourly" else start_date
        api_end = end_date + timedelta(days=1) if granularity == "hourly" else end_date
        params = {
            "latitude": lat, "longitude": lon,
            "start_date": api_start.isoformat(), "end_date": api_end.isoformat(),
            granularity: variables, "timezone": api_timezone,
        }
        responses = client.weather_api(ARCHIVE_URL, params=params)
        if not responses:
            return pd.DataFrame(columns=variables)
        response = responses[0]
        data = response.Hourly() if granularity == "hourly" else response.Daily()
        if data is None:
            return pd.DataFrame(columns=variables)
        if granularity == "hourly":
            index = hourly_index(data.Time(), data.TimeEnd(), data.Interval(), timezone)
        else:
            index = daily_index(data.Time(), data.TimeEnd(), data.Interval(), response.UtcOffsetSeconds())
        payload = {name: data.Variables(i).ValuesAsNumpy() for i, name in enumerate(variables)}
        result = pd.DataFrame(payload, index=index)
        result.index.name = "date"
        if granularity == "hourly":
            result = trim_hourly_to_local_dates(result, start_date, end_date, timezone)
        return result
