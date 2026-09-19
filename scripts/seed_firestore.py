"""
Seed script for FitGear Coach Firestore database.
"""
from google.cloud import firestore

# HARDCODED PROJECT ID as required by user directive
PROJECT_ID = "qwiklabs-gcp-03-bec4fda9e582"

SEED_GEAR = [
    {
        "id": "shoe_001",
        "name": "SpeedPro Trail Runner v3",
        "category": "shoes",
        "terrain": "trail",
        "price": 140.0,
        "rating": 4.8,
        "description": "Durable, high-grip trail running shoe with stone guard protection and responsive midsole.",
    },
    {
        "id": "shoe_002",
        "name": "Marathon Glide 5000",
        "category": "shoes",
        "terrain": "road",
        "price": 160.0,
        "rating": 4.7,
        "description": "Max-cushion road running shoe designed for long marathon training miles.",
    },
    {
        "id": "watch_001",
        "name": "Apex GPS Sport Watch",
        "category": "electronics",
        "terrain": "all-terrain",
        "price": 299.0,
        "rating": 4.9,
        "description": "Multisport GPS watch with wrist heart rate monitor, turn-by-turn navigation, and 40h battery.",
    },
    {
        "id": "pack_001",
        "name": "Hydration Vest Ultra 10L",
        "category": "accessories",
        "terrain": "trail",
        "price": 120.0,
        "rating": 4.6,
        "description": "Lightweight ergonomic hydration vest with twin 500ml flasks and trekking pole attachments.",
    },
]

SEED_WORKOUTS = [
    {
        "id": "plan_001",
        "title": "5K Trail Speed & Agility",
        "category": "trail running",
        "difficulty": "Intermediate",
        "duration_weeks": 4,
        "days_per_week": 4,
        "description": "Build hill power, technical descent agility, and 5K race pace velocity on trails.",
    },
    {
        "id": "plan_002",
        "title": "Beginner Endurance Base",
        "category": "road running",
        "difficulty": "Beginner",
        "duration_weeks": 6,
        "days_per_week": 3,
        "description": "Aerobic base building plan using low HR zone running and walk-run intervals.",
    },
]


def seed_database():
    db = firestore.Client(project=PROJECT_ID)
    print(f"Connecting to Firestore for project: {PROJECT_ID}")

    gear_ref = db.collection("gear_catalog")
    for item in SEED_GEAR:
        gear_ref.document(item["id"]).set(item)
        print(f"Seeded gear: {item['name']} ({item['id']})")

    workout_ref = db.collection("workout_plans")
    for plan in SEED_WORKOUTS:
        workout_ref.document(plan["id"]).set(plan)
        print(f"Seeded workout plan: {plan['title']} ({plan['id']})")

    print("✅ Firestore database seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
