from datetime import date

import pandas as pd

from src.data_processing import daily_index, export_table, hourly_index, trim_hourly_to_local_dates, validate_dates


def test_fall_back_has_25_hours_and_distinct_offsets():
    start = pd.Timestamp("2026-10-24 22:00", tz="UTC")
    end = pd.Timestamp("2026-10-25 23:00", tz="UTC")
    index = hourly_index(int(start.timestamp()), int(end.timestamp()), 3600, "Europe/Prague")
    assert len(index) == 25
    assert sum(t.hour == 2 for t in index) == 2
    frame = pd.DataFrame({"temperature_2m": range(25)}, index=index)
    exported = export_table(frame, "hourly")
    assert exported["Hour_Tag"].iloc[-1] == "H25"
    assert exported.loc[2, "Local_Time"] != exported.loc[3, "Local_Time"]


def test_spring_forward_has_23_hours():
    start = pd.Timestamp("2026-03-28 23:00", tz="UTC")
    end = pd.Timestamp("2026-03-29 22:00", tz="UTC")
    index = hourly_index(int(start.timestamp()), int(end.timestamp()), 3600, "Europe/Prague")
    assert len(index) == 23
    assert 2 not in {t.hour for t in index}


def test_local_daily_dates_and_column_order():
    start = pd.Timestamp("2026-02-01", tz="UTC")
    index = daily_index(int(start.timestamp()), int((start + pd.Timedelta(days=2)).timestamp()), 86400, 3600)
    assert list(index.strftime("%Y-%m-%d")) == ["2026-02-01", "2026-02-02"]
    table = export_table(pd.DataFrame({"precipitation_sum": [1, 2]}, index=index), "daily")
    assert table.columns.tolist() == ["datum", "precipitation_sum"]
    assert table.loc[0, "datum"] == "1.2.2026"


def test_invalid_date_range():
    assert validate_dates(date(2026, 5, 2), date(2026, 5, 1)) is not None


def test_czech_october_november_local_boundaries_are_exact():
    utc = pd.date_range("2026-10-04", "2026-11-04", freq="h", tz="UTC")
    frame = pd.DataFrame({"value": range(len(utc))}, index=utc)
    output = trim_hourly_to_local_dates(frame, date(2026, 10, 5), date(2026, 11, 2), "Europe/Prague")
    local = output.index.tz_convert("Europe/Prague")
    assert len(output) == 697
    assert local[0].strftime("%Y-%m-%d %H:%M %z") == "2026-10-05 00:00 +0200"
    assert local[-1].strftime("%Y-%m-%d %H:%M %z") == "2026-11-02 23:00 +0100"
    counts = pd.Series(1, index=local).groupby(local.date).sum()
    assert counts.loc[date(2026, 10, 25)] == 25
    assert counts.loc[date(2026, 10, 5)] == 24
    assert counts.loc[date(2026, 11, 2)] == 24
    assert set(counts.to_numpy()) == {24, 25}


def test_czech_spring_transition_keeps_23_hours():
    utc = pd.date_range("2026-03-28", "2026-03-31", freq="h", tz="UTC")
    frame = pd.DataFrame({"value": range(len(utc))}, index=utc)
    output = trim_hourly_to_local_dates(frame, date(2026, 3, 29), date(2026, 3, 29), "Europe/Prague")
    assert len(output) == 23
    assert output.index[0].tz_convert("Europe/Prague").hour == 0
    assert output.index[-1].tz_convert("Europe/Prague").hour == 23


def test_non_european_timezones_also_trim_correctly():
    utc = pd.date_range("2026-06-01", "2026-06-05", freq="h", tz="UTC")
    frame = pd.DataFrame({"value": range(len(utc))}, index=utc)
    for zone in ["Pacific/Auckland", "America/Los_Angeles", "Pacific/Honolulu"]:
        result = trim_hourly_to_local_dates(frame, date(2026, 6, 2), date(2026, 6, 3), zone)
        assert len(result) == 48
        assert result.index[0].tz_convert(zone).date() == date(2026, 6, 2)
        assert result.index[-1].tz_convert(zone).date() == date(2026, 6, 3)
