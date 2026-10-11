from collections import defaultdict
from src.models.exercise_day import ExerciseDay

METERS_PER_MILE = 1609.344

DISTANCE_THRESHOLDS = {
    "Walk": 2.0,
    "Ride": 5.0,
    "Hike": 2.0,
}

def calculate_exercise_days(activity_rows):
    # Each row contains database fields plus the Strava activity type.
    # The activity type is the last column returned by the repository.
    daily_distances = defaultdict(float)

    for row in activity_rows:
        start_date_local = row[7]
        distance_meters = row[3]
        activity_type = row[18]

        if start_date_local is None or distance_meters is None:
            continue

        activity_date = start_date_local.date()
        distance_miles = distance_meters / METERS_PER_MILE

        daily_distances[(activity_date, activity_type)] += distance_miles

    qualifying_days = defaultdict(list)
    qualifying_distances = defaultdict(float)

    for (activity_date, activity_type), total_miles in daily_distances.items():
        if activity_type == "Run":
            qualifies = True
        elif activity_type in DISTANCE_THRESHOLDS:
            qualifies = total_miles >= DISTANCE_THRESHOLDS[activity_type]
        else:
            qualifies = False

        if qualifies:
            qualifying_days[activity_date].append(activity_type)
            qualifying_distances[activity_date] += total_miles

    return [
        ExerciseDay(
            exercise_date=activity_date,
            qualifying_types=sorted(qualifying_days[activity_date]),
            total_distance_miles=qualifying_distances[activity_date],
        )
        for activity_date in sorted(qualifying_days)
    ]