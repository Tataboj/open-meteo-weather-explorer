"""Conservative single-input location resolution.

Never silently accept a fuzzy match such as Cheb -> Cheboksary.
"""

import unicodedata
from typing import Any


def _normalize(value: str) -> str:
    letters = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in letters if not unicodedata.combining(ch)).strip()


def normalize_search_query(query: str) -> str:
    """Translate known colloquial place names into geocoding search terms."""
    name = query.split(",", 1)[0].strip()
    aliases = {"hranice na morave": "Hranice", "praha": "Prague"}
    return aliases.get(_normalize(name), name)


def location_suggestions(query: str, locations: list[dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
    """Rank results by exact name and Czech locality, but show every choice explicitly."""
    name = _normalize(normalize_search_query(query))
    country = _normalize(query.split(",", 1)[1]) if "," in query else ""
    candidates = [
        item for item in locations
        if not country or country in {
            _normalize(str(item.get("country_code", ""))), _normalize(str(item.get("country", "")))
        }
    ]
    candidates.sort(key=lambda item: (
        _normalize(str(item.get("name", ""))) != name,
        item.get("country_code") != "CZ" if not country else False,
        -(item.get("population") or 0),
    ))
    result = []
    for item in candidates:
        label = f"{item.get('name', '?')} — {item.get('admin1') or item.get('country', '?')} ({item.get('country', '?')})"
        result.append((label, item))
    return result[:12]


def resolve_unambiguous_location(query: str, locations: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Resolve a typed name only when we have a defensible exact match.

    A unique Czech exact match is allowed to win over namesakes elsewhere.
    Otherwise ambiguous names require an explicit suggestion click.
    """
    name = _normalize(normalize_search_query(query))
    if len(name) < 2:
        return None
    country = _normalize(query.split(",", 1)[1]) if "," in query else None
    matches = [item for item in locations if _normalize(str(item.get("name", ""))) == name]
    if country:
        matches = [
            item for item in matches
            if country in {
                _normalize(str(item.get("country_code", ""))),
                _normalize(str(item.get("country", ""))),
            }
        ]
    if len(matches) == 1:
        return matches[0]
    if country is None:
        czech_matches = [item for item in matches if item.get("country_code") == "CZ"]
        if len(czech_matches) == 1:
            return czech_matches[0]
    return None


def choose_location(query: str, locations: list[dict[str, Any]]) -> dict[str, Any] | None:
    parts = [part.strip() for part in query.split(",", 1)]
    desired_name = _normalize(parts[0])
    country = _normalize(parts[1]) if len(parts) == 2 else None
    if not desired_name:
        return None
    exact = [item for item in locations if _normalize(str(item.get("name", ""))) == desired_name]
    if country:
        exact = [
            item for item in exact
            if country in {_normalize(str(item.get("country_code", ""))), _normalize(str(item.get("country", "")))}
        ]
    if not exact:
        return None
    # Czech location preference reflects the app's Czech-first audience.
    # If explicitly specified, the country filter above takes precedence.
    exact.sort(key=lambda item: (
        item.get("country_code") != "CZ" if country is None else False,
        -(item.get("population") or 0),
        str(item.get("id", "")),
    ))
    return exact[0]
