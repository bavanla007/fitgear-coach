"""
Pacing split calculator tool for FitGear Coach agent.
"""
from typing import Dict, Any

STANDARD_DISTANCES = {
    "5k": 5.0,
    "10k": 10.0,
    "half_marathon": 21.0975,
    "marathon": 42.195,
}


def calculate_race_splits(
    recent_distance: str,
    recent_time_minutes: float,
    target_distance: str = "10k",
) -> Dict[str, Any]:
    """
    Calculate predicted race finish time, target pace per km/mile using Riegel's formula.

    Args:
        recent_distance: Distance of recent race ('5k', '10k', 'half_marathon', 'marathon').
        recent_time_minutes: Time achieved in recent race in total minutes (e.g. 22.5).
        target_distance: Target race distance ('5k', '10k', 'half_marathon', 'marathon').

    Returns:
        Dictionary containing predicted time, average pace per km/mile, and pacing targets.
    """
    d1 = STANDARD_DISTANCES.get(recent_distance.lower().replace(" ", "_"), 5.0)
    d2 = STANDARD_DISTANCES.get(target_distance.lower().replace(" ", "_"), 10.0)

    # Riegel's formula: T2 = T1 * (D2 / D1) ^ 1.06
    predicted_minutes = recent_time_minutes * ((d2 / d1) ** 1.06)

    pace_per_km_min = predicted_minutes / d2
    pace_per_mile_min = pace_per_km_min * 1.60934

    def format_time(mins: float) -> str:
        h = int(mins // 60)
        m = int(mins % 60)
        s = int(round((mins - int(mins)) * 60))
        if s == 60:
            m += 1
            s = 0
        if h > 0:
            return f"{h}h {m:02d}m {s:02d}s"
        return f"{m}m {s:02d}s"

    return {
        "recent_distance": recent_distance,
        "recent_time": format_time(recent_time_minutes),
        "target_distance": target_distance,
        "predicted_finish_time": format_time(predicted_minutes),
        "target_pace_per_km": f"{format_time(pace_per_km_min)} / km",
        "target_pace_per_mile": f"{format_time(pace_per_mile_min)} / mi",
    }
