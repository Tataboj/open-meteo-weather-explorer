"""Excel export without timezone-aware Excel cells."""

from io import BytesIO

import pandas as pd

from .data_processing import export_table


def create_excel(df: pd.DataFrame, granularity: str) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        export_table(df, granularity).to_excel(writer, sheet_name="Weather_Data", index=False)
    return buffer.getvalue()
