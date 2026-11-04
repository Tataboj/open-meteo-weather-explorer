# v1.0.0 release and online deployment checklist

**STATUS: PREPARED — NOT PUBLISHED.** Separate owner authorization is required for public repository publication, push, deployment, and tag/release.

## Preflight

- [ ] Verify source hygiene, screenshot privacy, dependency licenses, and absence of secrets.
- [ ] Verify tests on Python 3.12: `python -m pytest -q`.
- [ ] Confirm Windows `run.bat` works in a clean folder with Python 3.12.
- [ ] Test location search, chart, and Excel download with a real API response.
- [ ] Check DST Excel export: 2026-10-25 in Prague has 25 hours, ordinary days 24, and no dates spill past the requested range.
- [ ] Confirm MIT/Tataboj attribution and current Open-Meteo data terms.

## GitHub publication (separate approval)

- [ ] Confirm exact GitHub account, repository, and public/private setting.
- [ ] Review the exact set of files in GitHub Desktop before commit/publish.
- [ ] Publish repository and verify files and CI at the remote commit.
- [ ] Create separately authorized `v1.0.0` tag and GitHub Release; verify downloadable archive.

## Streamlit Community Cloud (separate approval)

- [ ] Use the approved GitHub repository and entrypoint `app.py`.
- [ ] Configure Python 3.12 and dependency installation from root `requirements.txt`.
- [ ] Test live search, weather retrieval, chart, Excel export, and DST correctness.
- [ ] Check Open-Meteo fair-usage conditions for the intended audience.
- [ ] Add verified live URL to README only after deployment passes.

**GitHub repository ≠ live Streamlit app ≠ tagged GitHub release.**
