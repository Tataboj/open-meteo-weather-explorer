"""Streamlit entry point for the historical weather explorer."""

from datetime import date, timedelta

import plotly.express as px
import streamlit as st
from streamlit_searchbox import st_searchbox

from src.config import DAILY_VARIABLES, HOURLY_VARIABLES
from src.data_processing import validate_dates
from src.excel_export import create_excel
from src.location_matching import location_suggestions, resolve_unambiguous_location
from src.weather_service import WeatherDataService


st.set_page_config(
    page_title="Open-Meteo Weather Explorer",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Historická meteorologická data poskytuje Open-Meteo."},
)

VARIABLE_LABELS = {
    "temperature_2m": "Teplota (°C)",
    "relative_humidity_2m": "Relativní vlhkost (%)",
    "precipitation": "Srážky (mm)",
    "wind_speed_10m": "Rychlost větru (km/h)",
    "temperature_2m_max": "Maximální teplota (°C)",
    "temperature_2m_min": "Minimální teplota (°C)",
    "precipitation_sum": "Úhrn srážek (mm)",
    "wind_speed_10m_max": "Maximální rychlost větru (km/h)",
}


@st.cache_data(ttl=3600, show_spinner=False)
def search_locations(query: str) -> list[tuple[str, dict]]:
    if len(query.strip()) < 2:
        return []
    with st.spinner("Hledám dostupná místa…"):
        return location_suggestions(query, WeatherDataService.get_coordinates(query))


@st.cache_data(ttl=3600, show_spinner=False)
def resolve_typed_location(query: str) -> dict | None:
    if len(query.strip()) < 2:
        return None
    with st.spinner("Ověřuji zadané město…"):
        return resolve_unambiguous_location(query, WeatherDataService.get_coordinates(query))


def main() -> None:
    st.title("🌡️ Open-Meteo Weather Explorer")
    st.caption("Vyberte město, období a meteorologické veličiny. Výsledky si můžete stáhnout do Excelu.")

    with st.sidebar:
        st.header("1. Lokalita")
        st.caption("Začněte psát název města. Z našeptávače vyberte správnou lokalitu.")
        selected_location = st_searchbox(
            search_locations,
            placeholder="Například Cheb nebo Hranice na Moravě",
            label="Zadejte název místa",
            key="location_search",
            default_searchterm="",
            default_use_searchterm=True,
            debounce=350,
            edit_after_submit="option",
            clear_on_submit=False,
        )
        if isinstance(selected_location, dict):
            location = selected_location
        elif isinstance(selected_location, str):
            try:
                location = resolve_typed_location(selected_location)
            except Exception as exc:
                location = None
                st.warning(f"Vyhledávání se nezdařilo: {exc}")
        else:
            location = None

        st.divider()
        st.header("2. Časový rozsah")
        start_date = st.date_input("Od", date.today() - timedelta(days=30))
        end_date = st.date_input("Do", date.today() - timedelta(days=2))
        st.divider()
        st.header("3. Granularita")
        granularity = "hourly" if st.radio("Frekvence", ["Hodinová", "Denní"], horizontal=True) == "Hodinová" else "daily"
        options = HOURLY_VARIABLES if granularity == "hourly" else DAILY_VARIABLES
        variables = st.multiselect("Meteorologické veličiny", options, default=[options[0]], format_func=lambda name: VARIABLE_LABELS.get(name, name))

    error = validate_dates(start_date, end_date)
    if error:
        st.error(error)
        return
    if location is None:
        st.info("🔎 Zadejte název města a vyberte správnou lokalitu z nabídky našeptávače.")
        return
    if not variables:
        st.info("Vyberte alespoň jednu meteorologickou veličinu.")
        return

    timezone = location.get("timezone") or "UTC"
    st.info(f"📍 {location['name']} ({location.get('country', '')}) — časové pásmo: {timezone}")
    try:
        with st.spinner("Načítám historická data z Open-Meteo…", show_time=True):
            df = WeatherDataService.fetch_historical_data(
                location["latitude"], location["longitude"],
                start_date, end_date, variables, granularity, timezone,
            )
        if df.empty:
            st.warning("Pro zvolený rozsah nejsou dostupná data.")
            return
        chart = px.line(df.rename(columns=VARIABLE_LABELS), x=df.index, y=[VARIABLE_LABELS.get(name, name) for name in variables])
        chart.update_layout(xaxis_title=f"Čas ({timezone})", yaxis_title="Naměřená hodnota", legend_title_text="Veličina")
        st.plotly_chart(chart, width="stretch")
        with st.expander("Tabulka dat"):
            st.dataframe(df, width="stretch")

        excel = create_excel(df, granularity)
        safe_city = "".join(c if c.isalnum() or c in "-_" else "_" for c in location["name"])
        st.download_button(
            "Stáhnout Excel (.xlsx)", excel,
            file_name=f"Weather_{safe_city}_{start_date}_to_{end_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as exc:
        st.error(f"Načítání nebo export dat selhal: {exc}")


if __name__ == "__main__":
    main()
