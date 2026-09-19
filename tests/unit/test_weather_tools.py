"""
Unit test for Open-Meteo weather tools.
"""
from app.tools.weather_tools import get_outdoor_running_conditions


def test_get_outdoor_running_conditions():
    res = get_outdoor_running_conditions("Boston")
    assert "city" in res
    assert "temperature_fahrenheit" in res
    assert "conditions_summary" in res
    assert res["error"] is None if "error" in res else True
