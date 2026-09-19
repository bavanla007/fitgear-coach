"""
Firestore tools for FitGear Coach agent.
"""
from typing import Dict, Any, List, Optional
from google.cloud import firestore

# HARDCODED PROJECT ID as required by user directive
PROJECT_ID = "qwiklabs-gcp-03-bec4fda9e582"

_db_client: Optional[firestore.Client] = None


def get_firestore_client() -> firestore.Client:
    """Returns cached Firestore Client initialized with hardcoded project ID."""
    global _db_client
    if _db_client is None:
        _db_client = firestore.Client(project=PROJECT_ID)
    return _db_client


def search_gear_catalog(
    category: Optional[str] = None,
    terrain: Optional[str] = None,
    max_price: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Search gear catalog in Firestore database by category, terrain, or max price.

    Args:
        category: Filter by category (e.g. 'shoes', 'electronics', 'accessories').
        terrain: Filter by terrain (e.g. 'trail', 'road', 'all-terrain').
        max_price: Filter items with price <= max_price.

    Returns:
        List of matching gear items with details.
    """
    db = get_firestore_client()
    query = db.collection("gear_catalog")
    if category:
        query = query.where("category", "==", category.lower())
    if terrain:
        query = query.where("terrain", "==", terrain.lower())

    docs = query.stream()
    results = []
    for doc in docs:
        data = doc.to_dict()
        if max_price is not None and data.get("price", 0) > max_price:
            continue
        results.append(data)
    return results


def add_gear_item(
    item_id: str,
    name: str,
    category: str,
    terrain: str,
    price: float,
    description: str,
    rating: float = 5.0,
) -> Dict[str, Any]:
    """
    Add or update a gear item in the Firestore gear catalog.

    Args:
        item_id: Unique string ID for the gear (e.g. 'shoe_003').
        name: Name of the gear.
        category: Category (e.g. 'shoes', 'electronics', 'accessories').
        terrain: Suitable terrain (e.g. 'trail', 'road', 'gym').
        price: Price in USD.
        description: Detailed summary of features and use cases.
        rating: Rating out of 5.0 (default 5.0).

    Returns:
        Confirmation dictionary with the saved item data.
    """
    db = get_firestore_client()
    item_data = {
        "id": item_id,
        "name": name,
        "category": category.lower(),
        "terrain": terrain.lower(),
        "price": float(price),
        "description": description,
        "rating": float(rating),
    }
    db.collection("gear_catalog").document(item_id).set(item_data)
    return {"status": "success", "item": item_data}


def get_workout_plans(
    difficulty: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Fetch workout plans from Firestore database, optionally filtered by difficulty.

    Args:
        difficulty: Filter by difficulty level ('Beginner', 'Intermediate', 'Advanced').

    Returns:
        List of workout plan objects.
    """
    db = get_firestore_client()
    query = db.collection("workout_plans")
    if difficulty:
        query = query.where("difficulty", "==", difficulty.title())

    docs = query.stream()
    results = [doc.to_dict() for doc in docs]
    return results
