from io import BytesIO

import pandas as pd

from src.excel_export import create_excel


def test_excel_round_trip():
    index = pd.date_range("2026-06-01", periods=2, freq="h", tz="Europe/Prague")
    data = pd.DataFrame({"temperature_2m": [20.0, 21.0]}, index=index)
    content = create_excel(data, "hourly")
    table = pd.read_excel(BytesIO(content))
    assert table.columns.tolist() == ["datum", "Hour_Tag", "Local_Time", "temperature_2m"]
    assert table["Hour_Tag"].tolist() == ["H01", "H02"]
