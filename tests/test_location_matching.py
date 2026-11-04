from src.location_matching import choose_location, location_suggestions, normalize_search_query, resolve_unambiguous_location


LOCATIONS = [
    {"name": "Cheboksary", "country": "Russia", "country_code": "RU", "population": 500000},
    {"name": "Cheb", "country": "Czechia", "country_code": "CZ", "population": 31000},
    {"name": "Cheb", "country": "United States", "country_code": "US", "population": 100},
]


def test_cheb_selects_czechia_not_russia():
    assert choose_location("Cheb", LOCATIONS)["country_code"] == "CZ"


def test_explicit_country_takes_precedence():
    assert choose_location("Cheb, US", LOCATIONS)["country_code"] == "US"


def test_fuzzy_match_is_rejected():
    assert choose_location("Che", LOCATIONS) is None


def test_no_second_choice_needed():
    assert choose_location("Cheb, CZ", LOCATIONS)["name"] == "Cheb"


def test_alias_for_hranice_na_morave():
    assert normalize_search_query("Hranice na Moravě") == "Hranice"


def test_praha_alias():
    assert normalize_search_query("Praha") == "Prague"


def test_suggestions_prioritize_exact_czech_city():
    suggestions = location_suggestions("Cheb", LOCATIONS)
    assert suggestions[0][1]["country_code"] == "CZ"
    assert "Czechia" in suggestions[0][0]


def test_country_filter_in_suggestions():
    suggestions = location_suggestions("Cheb, US", LOCATIONS)
    assert len(suggestions) == 1
    assert suggestions[0][1]["country_code"] == "US"


def test_enter_cheb_autoselects_czech_match():
    assert resolve_unambiguous_location("Cheb", LOCATIONS)["country_code"] == "CZ"


def test_enter_does_not_choose_fuzzy_city():
    assert resolve_unambiguous_location("Che", LOCATIONS) is None


def test_ambiguous_exact_names_require_click():
    cities = [
        {"name": "Springfield", "country_code": "US", "id": 1},
        {"name": "Springfield", "country_code": "US", "id": 2},
    ]
    assert resolve_unambiguous_location("Springfield", cities) is None


def test_enter_praha_selects_czech_prague():
    cities = [
        {"name": "Prague", "country_code": "US"},
        {"name": "Prague", "country_code": "CZ"},
    ]
    assert resolve_unambiguous_location("Praha", cities)["country_code"] == "CZ"
