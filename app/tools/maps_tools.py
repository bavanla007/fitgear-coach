"""
Google Maps Geocoding and Places API (New) tools for FitGear Coach agent.
"""
from typing import Dict, Any, List, Optional
import os
import urllib.request
import urllib.parse
import json


def _get_api_key() -> str:
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set.")
    return key


def geocode_address(address: str) -> Dict[str, Any]:
    """
    Convert a street address or location name into geographic coordinates (lat/lng).

    Args:
        address: Street address or location name (e.g. '1600 Amphitheatre Pkwy, Mountain View, CA' or 'Central Park, NY').

    Returns:
        Dictionary containing formatted address, latitude, and longitude.
    """
    try:
        api_key = _get_api_key()
        encoded_address = urllib.parse.quote(address)
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address}&key={api_key}"

        req = urllib.request.Request(url, headers={"User-Agent": "FitGearCoach/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        if data.get("status") != "OK" or not data.get("results"):
            return {"error": f"Geocoding failed for address '{address}': {data.get('status', 'No results')}"}

        result = data["results"][0]
        location = result["geometry"]["location"]

        return {
            "address": result.get("formatted_address"),
            "location": {
                "latitude": location.get("lat"),
                "longitude": location.get("lng"),
            },
        }
    except Exception as e:
        return {"error": f"Geocoding request error: {str(e)}"}


def find_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "park",
    radius_meters: float = 3000.0,
) -> List[Dict[str, Any]]:
    """
    Find nearby places (e.g. parks, gym, sporting_goods_store) using Google Places API (New).

    Args:
        latitude: Center latitude coordinate.
        longitude: Center longitude coordinate.
        place_type: Type of place to search for (e.g. 'park', 'gym', 'sporting_goods_store').
        radius_meters: Search radius in meters (default 3000m / 3km).

    Returns:
        List of nearby places with name, formatted address, and location coordinates.
    """
    try:
        api_key = _get_api_key()
        url = "https://places.googleapis.com/v1/places:searchNearby"

        body = json.dumps({
            "includedTypes": [place_type.lower()],
            "maxResultCount": 10,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": float(latitude),
                        "longitude": float(longitude),
                    },
                    "radius": float(radius_meters),
                }
            },
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
            "User-Agent": "FitGearCoach/1.0",
        }

        req = urllib.request.Request(url, data=body, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        places_raw = data.get("places", [])
        results = []
        for p in places_raw:
            name = p.get("displayName", {}).get("text", "Unknown")
            addr = p.get("formattedAddress", "")
            loc = p.get("location", {})
            results.append({
                "name": name,
                "address": addr,
                "location": {
                    "latitude": loc.get("latitude"),
                    "longitude": loc.get("longitude"),
                },
            })

        return results
    except Exception as e:
        return [{"error": f"Places search failed: {str(e)}"}]
