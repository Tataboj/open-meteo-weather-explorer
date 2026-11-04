"""Validation and time-axis helpers.

Hourly Open-Meteo requests use UTC so timestamps represent unambiguous instants.
Daily requests use the location timezone for correct local-day aggregation.
"""

from datetime import date, timedelta

import pandas as pd


def validate_dates(start: date, end: date) -> str | None:
    if start > end:
        return "Datum 'Od' nesmí být později než datum 'Do'."
    if end >= date.today():
        return "Historická data vybírejte nejpozději do včerejška; nedávná data mohou být neúplná."
    return None


def hourly_index(start_epoch: int, end_epoch: int, interval_seconds: int, timezone: str) -> pd.DatetimeIndex:
    if interval_seconds <= 0:
        raise ValueError("Invalid hourly interval")
    utc_index = pd.date_range(
        start=pd.to_datetime(start_epoch, unit="s", utc=True),
        end=pd.to_datetime(end_epoch, unit="s", utc=True),
        freq=pd.Timedelta(seconds=int(interval_seconds)), inclusive="left",
    )
    return utc_index.tz_convert(timezone)


def trim_hourly_to_local_dates(df: pd.DataFrame, start: date, end: date, timezone: str) -> pd.DataFrame:
    """Keep all and only hourly observations in the requested local calendar days.

    Local midnight boundaries are converted independently to UTC. This keeps
    23/25-hour DST transition days intact and discards API padding days.
    """
    if start > end:
        raise ValueError("Start date must be on or before end date")
    if df.index.tz is None:
        raise ValueError("Hourly data must have a timezone-aware index")
    first = pd.Timestamp(start).tz_localize(timezone)
    after_last = pd.Timestamp(end + timedelta(days=1)).tz_localize(timezone)
    return df.loc[(df.index >= first) & (df.index < after_last)].copy()


def daily_index(start_epoch: int, end_epoch: int, interval_seconds: int, utc_offset_seconds: int) -> pd.DatetimeIndex:
    """Decode local calendar days from Open-Meteo's local-time encoded epochs."""
    if interval_seconds <= 0:
        raise ValueError("Invalid daily interval")
    encoded = pd.date_range(
        start=pd.to_datetime(start_epoch, unit="s", utc=True),
        end=pd.to_datetime(end_epoch, unit="s", utc=True),
        freq=pd.Timedelta(seconds=int(interval_seconds)), inclusive="left",
    )
    return (encoded + pd.Timedelta(seconds=int(utc_offset_seconds))).tz_localize(None).normalize()


def export_table(df: pd.DataFrame, granularity: str) -> pd.DataFrame:
    if granularity not in {"hourly", "daily"}:
        raise ValueError("Unknown granularity")
    exported = df.copy()
    exported.insert(0, "datum", [f"{dt.day}.{dt.month}.{dt.year}" for dt in df.index])
    if granularity == "hourly":
        ranks = exported.groupby(exported["datum"], sort=False).cumcount() + 1
        exported.insert(1, "Hour_Tag", [f"H{number:02d}" for number in ranks])
        exported.insert(2, "Local_Time", [dt.strftime("%H:%M %z") for dt in df.index])
    # Excel cannot store timezone-aware datetimes; explicit date/time columns
    # retain the crucial DST offset information in hourly exports.
    return exported.reset_index(drop=True)
