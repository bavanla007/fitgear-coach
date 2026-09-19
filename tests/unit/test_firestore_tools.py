"""
Unit tests for Firestore tools.
"""
from app.tools.firestore_tools import search_gear_catalog, add_gear_item, get_workout_plans


def test_firestore_gear_tools():
    # Test reading seeded items
    gear_items = search_gear_catalog()
    assert isinstance(gear_items, list)
    assert len(gear_items) >= 4

    # Test adding new item
    new_item = add_gear_item(
        item_id="test_shoe_99",
        name="Test Racer 100",
        category="shoes",
        terrain="road",
        price=199.99,
        description="High speed road racing shoe.",
        rating=5.0,
    )
    assert new_item["status"] == "success"
    assert new_item["item"]["id"] == "test_shoe_99"

    # Test query newly added item
    road_shoes = search_gear_catalog(category="shoes", terrain="road")
    item_ids = [item["id"] for item in road_shoes]
    assert "test_shoe_99" in item_ids


def test_firestore_workout_tools():
    plans = get_workout_plans()
    assert isinstance(plans, list)
    assert len(plans) >= 2
