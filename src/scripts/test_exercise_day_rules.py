from datetime import datetime
from src.services.exercise_day_calculator import calculate_exercise_days

METERS_PER_MILE = 1609.344

def make_activity(activity_date, activity_type, miles):
    """Create a database-style row for testing the calculator."""
    row = [None] * 19
    row[3] = miles * METERS_PER_MILE
    row[7] = datetime.fromisoformat(f"{activity_date}T12:00:00")
    row[18] = activity_type
    return tuple(row)

def main():
    # Test 1: Two short walks combine to meet the 2-mile threshold.
    activities = [
        make_activity("2026-01-01", "Walk", 1.0),
        make_activity("2026-01-01", "Walk", 1.5),
    ]

    results = calculate_exercise_days(activities)

    assert len(results) == 1
    assert results[0].exercise_date.isoformat() == "2026-01-01"
    assert "Walk" in results[0].qualifying_types

    print("PASS: Two walks aggregate to qualify.")

    # Test 2: A walk and hike do not combine to meet either threshold.
    activities = [
        make_activity("2026-01-02", "Walk", 1.0),
        make_activity("2026-01-02", "Hike", 1.5),
    ]

    results = calculate_exercise_days(activities)

    assert len(results) == 0

    print("PASS: Different activity types do not aggregate together.")

    # Test 3: A short run qualifies regardless of distance.
    activities = [
        make_activity("2026-01-03", "Run", 0.5),
    ]

    results = calculate_exercise_days(activities)

    assert len(results) == 1
    assert results[0].exercise_date.isoformat() == "2026-01-03"
    assert "Run" in results[0].qualifying_types

    print("PASS: A short run qualifies.")

    # Test 4: A walk exactly at 2 miles qualifies.
    activities = [
        make_activity("2026-01-04", "Walk", 2.0),
    ]

    results = calculate_exercise_days(activities)
    assert len(results) == 1
    print("PASS: A 2-mile walk qualifies.")

    # Test 5: A walk below 2 miles does not qualify.
    activities = [
        make_activity("2026-01-05", "Walk", 1.99),
    ]

    results = calculate_exercise_days(activities)
    assert len(results) == 0
    print("PASS: A walk below 2 miles does not qualify.")

    # Test 6: A ride exactly at 5 miles qualifies.
    activities = [
        make_activity("2026-01-06", "Ride", 5.0),
    ]

    results = calculate_exercise_days(activities)
    assert len(results) == 1
    print("PASS: A 5-mile ride qualifies.")

    # Test 7: A hike exactly at 2 miles qualifies.
    activities = [
        make_activity("2026-01-07", "Hike", 2.0),
    ]

    results = calculate_exercise_days(activities)
    assert len(results) == 1
    print("PASS: A 2-mile hike qualifies.")
    print()
    print("All seven Exercise Day rule tests passed!")

if __name__ == "__main__":
    main()