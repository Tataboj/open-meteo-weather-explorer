from unittest.mock import Mock, patch

from src.weather_service import WeatherDataService


def test_geocoding_empty_response():
    response = Mock()
    response.json.return_value = {}
    with patch.object(WeatherDataService, "_session") as session:
        session.return_value.get.return_value = response
        assert WeatherDataService.get_coordinates("missing") == []
