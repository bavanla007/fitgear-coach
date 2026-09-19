"""
Unit tests for pacing calculator tool.
"""
from app.tools.pacing_tools import calculate_race_splits


def test_calculate_race_splits():
    # 5K in 20 minutes -> calculate 10K prediction
    res = calculate_race_splits("5k", 20.0, "10k")
    assert res["target_distance"] == "10k"
    assert "predicted_finish_time" in res
    assert "target_pace_per_km" in res
    assert "target_pace_per_mile" in res
