"""
Unit tests for Maps Geocoding and Places API tools.
"""
from app.tools.maps_tools import geocode_address, find_nearby_places


def test_geocode_address():
    res = geocode_address("Boston Common, MA")
    assert "address" in res
    assert "location" in res
    assert res["location"]["latitude"] is not None
    assert res["location"]["longitude"] is not None


def test_find_nearby_places():
    places = find_nearby_places(42.3550897, -71.0657256, place_type="park", radius_meters=2000)
    assert isinstance(places, list)
    assert len(places) > 0
    assert "name" in places[0]
    assert "address" in places[0]
    assert "location" in places[0]
