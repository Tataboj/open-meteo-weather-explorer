
# 🌡️ Open-Meteo Weather Explorer

**Version 1.0.0 · Developed by Tataboj · MIT License**

### 🚀 [Launch Online Demo — Run in Your Browser](https://open-meteo-weather-explorer-tataboj.streamlit.app)

**Try the application online for free. No installation, GitHub account, or registration required.**

[![Live Demo](https://img.shields.io/badge/Launch-Live%20Demo-brightgreen?style=for-the-badge)](https://open-meteo-weather-explorer-tataboj.streamlit.app)
[![GitHub Release](https://img.shields.io/badge/Release-v1.0.0-blue?style=for-the-badge)](https://github.com/Tataboj/open-meteo-weather-explorer/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

![Actual application screenshot: weather chart for Cheb, Czechia](screenshots/weather-explorer-cheb.png)

> **🌐 Live Demo:** [Open-Meteo Weather Explorer on Streamlit Cloud](https://open-meteo-weather-explorer-tataboj.streamlit.app)
>
> **⬇️ Download v1.0.0:** [Official GitHub Release](https://github.com/Tataboj/open-meteo-weather-explorer/releases/tag/v1.0.0). Download the source code ZIP from the release assets, or use **Code → Download ZIP** for the latest source.
>
> **⏳ Startup time:** When the online application is asleep, Streamlit Community Cloud may need some time to wake it up. Please wait for the application to load.

## About the project

Open-Meteo Weather Explorer is an open-source historical weather data application built with **Python, Streamlit, pandas, and Plotly**.

It allows users to:

- Search for locations worldwide.
- Explore historical weather conditions.
- Visualize hourly and daily meteorological data.
- Display timestamps in each location's local timezone.
- Export weather data to Microsoft Excel (`.xlsx`).

The application is designed for anyone who wants to explore historical weather data through an interactive interface without writing Python code.

The user interface is primarily in Czech.

**Author:** Tataboj  
**Version:** 1.0.0  
**License for original source code:** [MIT](LICENSE)  
**Weather data provider:** [Open-Meteo](https://open-meteo.com/)  
**Hosting:** Streamlit Community Cloud

Open-Meteo data have their own licensing and attribution requirements. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

This is an independent project and is not affiliated with or endorsed by Open-Meteo.

## 🚀 Run online

The application is publicly available at:

### [Open Open-Meteo Weather Explorer](https://open-meteo-weather-explorer-tataboj.streamlit.app)

**Online users do not need to:**

- Install Python.
- Download the source code.
- Create a GitHub account.
- Register with Streamlit.
- Configure a local environment.

Simply open the link in a web browser.

### First launch and sleeping applications

The public demo runs on Streamlit Community Cloud.

To conserve server resources, Streamlit may put an application to sleep after a period of inactivity.

When this happens:

1. Open the application URL.
2. If Streamlit displays a wake-up screen, follow its instructions.
3. Wait for the application to start.
4. Once loaded, select a location and explore the weather data.

**A sleeping application may take a minute or longer to become available.**

This is normal behavior on shared cloud hosting and does not necessarily indicate an application error.

The initial deployment or installation of dependencies may take longer than an ordinary application restart.

## Features

### 🌍 Location search

- Single-field autocomplete powered by the Open-Meteo geocoding API.
- Search for cities and locations worldwide.
- Suggestions include the actual place, region, and country.
- Czech-first ranking for exact matches.
- Select a suggestion when multiple locations match.
- Known Czech alias `Hranice na Moravě` is searched as `Hranice`.
- A country suffix such as `Cheb, CZ` can help limit location candidates.
- Unambiguous exact matches can also be resolved by the backend when the search widget exposes the entered text.

### 📊 Historical weather charts

- Interactive charts powered by Plotly.
- Hourly and daily weather data.
- Temperature, humidity, precipitation, and wind speed.
- Daily maximum and minimum temperatures.
- Daily precipitation and maximum wind speed.
- User-selectable date ranges and meteorological variables.

### 🕒 Local timezones and daylight saving time

- Weather timestamps are displayed in the selected location's timezone.
- DST-aware processing handles days containing 23, 24, or 25 hours.
- Hourly timestamps remain unambiguous during daylight saving time transitions.
- Requested date ranges are processed using local calendar dates.

### 📥 Excel export

- Download weather results in `.xlsx` format.
- Czech-style date formatting.
- Local timestamps with explicit UTC offsets.
- Correct handling of daylight saving time transitions.

### 🖥️ User interface

- Czech-language controls and location search.
- Clean initial screen.
- No weather-data network request until the user searches.
- Loading indicators during location search and weather-data retrieval.
- Reduced developer toolbar.

## Run locally

You can also download the source code and run the application on your own computer.

### Requirements

- **Python 3.12**
- Internet connection
- Windows, macOS, or Linux

An internet connection is needed during dependency installation and for weather-data requests.

### Windows — quick start

> ⏳ **First launch: allow approximately 1–3 minutes, sometimes longer.**
>
> On the first run, the launcher creates a Python environment and downloads the required libraries. The time depends on your computer and internet connection.
>
> Subsequent launches are normally faster because the dependencies are already installed.
>
> Keep the terminal window open while the application is running.

**Instructions:**

1. Install **Python 3.12** from [python.org](https://www.python.org/downloads/) with the Windows `py` launcher.
2. Open the [GitHub Release v1.0.0](https://github.com/Tataboj/open-meteo-weather-explorer/releases/tag/v1.0.0).
3. Download **Source code (zip)** from the release assets.
4. Extract the ZIP archive to a folder on your computer.
5. Open the extracted project folder.
6. Double-click **`run.bat`**.
7. Wait for the application to start.

The application should open automatically in your browser.

If it does not, open:

http://localhost:8501

To stop the application, press `Ctrl+C` in the terminal.

**Important:** Do not run the launcher directly from inside the ZIP archive. Extract the files first.

Only run downloaded scripts from sources you trust.

### Windows — manual installation using PowerShell

Open PowerShell in the project directory.

Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the application:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open:

http://localhost:8501

Stop the application with `Ctrl+C`.

### macOS / Linux

Open a terminal in the project directory.

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

Install dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Start the application:

```bash
.venv/bin/python -m streamlit run app.py
```

Open:

http://localhost:8501

Stop the server with `Ctrl+C`.

## Tests

The project contains automated Python tests.

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the test suite:

```bash
python -m pytest -q
```

The tests cover:

- Daylight saving time transitions.
- Excel export.
- Date validation.
- Mocked geocoding responses.

External API connectivity is not included in the unit tests.

The release candidate passed the automated tests, and the GitHub Actions workflow completed successfully.

The public Streamlit deployment was also manually verified in a browser, including location selection, weather visualization, and Excel download.

## Deploy your own copy

You can deploy your own instance of Open-Meteo Weather Explorer using Streamlit Community Cloud.

### Deployment steps

1. Fork this repository to your own GitHub account.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub.
4. Create a new application using your fork.
5. Select your repository and branch.
6. Set the main file path to `app.py`.
7. Select Python **3.12** in Advanced settings.
8. Deploy the application.
9. Verify that location search, charts, and Excel export work correctly.

The application does not require a private API key for its public Open-Meteo data requests.

No Streamlit secrets are required for this project's standard configuration.

**Note:** Streamlit Community Cloud is a separate hosting service. Publishing a GitHub repository does not automatically deploy a running application.

For additional information, see the [deployment and release checklist](docs/DEPLOYMENT.md).

## Project layout

```text
app.py                  Streamlit user interface
src/config.py           API endpoints and variable lists
src/weather_service.py  Open-Meteo API client
src/data_processing.py  Timezone, date and export transformations
src/excel_export.py      XLSX generation
tests/                  Automated Python tests
.github/workflows/      GitHub Actions CI tests
screenshots/            Screenshot of the actual application
docs/                   Deployment/release checklist
run.bat                 Windows quick-start launcher
requirements.txt        Application dependencies
requirements-dev.txt    Development and test dependencies
LICENSE                 MIT license for original code
THIRD_PARTY_NOTICES.md  Third-party and data licensing notices
CHANGELOG.md            Version history
```

## Notes and limitations

- Historical archive availability varies by date, location, and weather variable.
- Weather data is obtained from the Open-Meteo API and requires an internet connection.
- Hourly data is retrieved in UTC and converted to the selected location's timezone.
- Daily data is requested in the location's timezone for local calendar-day aggregation.
- Hourly API requests include a one-day UTC buffer at each end and are then trimmed to the requested local calendar dates.
- This supports 23-hour spring-forward days, normal 24-hour days, and 25-hour fall-back days without including data outside the requested date range.
- `.cache/` and `.venv/` are local directories excluded from Git tracking.
- Python dependencies use compatible version ranges rather than a fully locked transitive environment.
- Streamlit Community Cloud uses shared hosting resources; startup times and performance may vary.
- The public demo may sleep after a period of inactivity and require a short wake-up period.
- Open-Meteo API availability and usage are subject to the provider's terms.

## License and attribution

**Copyright © 2026 Tataboj**

The original application source code is released under the **MIT License**.

See [LICENSE](LICENSE) for the complete license text.

Third-party Python packages retain their own licenses.

Weather and location data are provided by [Open-Meteo](https://open-meteo.com/) and remain subject to the provider's applicable licensing, attribution, and usage terms.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for additional information.

This project is independent and is not affiliated with or endorsed by Open-Meteo.

## Official links

- **Live application:** https://open-meteo-weather-explorer-tataboj.streamlit.app
- **GitHub repository:** https://github.com/Tataboj/open-meteo-weather-explorer
- **Official v1.0.0 release:** https://github.com/Tataboj/open-meteo-weather-explorer/releases/tag/v1.0.0
- **Open-Meteo:** https://open-meteo.com/

---

**Open-Meteo Weather Explorer v1.0.0 — Developed by Tataboj**
