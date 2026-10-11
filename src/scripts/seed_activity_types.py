from src.database.connection import get_connection
from src.models.activity_type import ActivityType

activity_types = [
    ActivityType(None, "Walk", "Walk"),
    ActivityType(None, "Run", "Run"),
    ActivityType(None, "Ride", "Ride"),
    ActivityType(None, "Hike", "Hike"),
    ActivityType(None, "Workout", "Workout"),
    ActivityType(None, "WeightTraining", "Weight Training"),
    ActivityType(None, "AlpineSki", "Alpine Ski"),
    ActivityType(None, "Elliptical", "Elliptical"),
    ActivityType(None, "EBikeRide", "E-Bike Ride"),
    ActivityType(None, "Yoga", "Yoga"),
    ActivityType(None, "Canoeing", "Canoeing"),
]

with get_connection() as connection:
    with connection.cursor() as cursor:
        for activity_type in activity_types:
            cursor.execute(
                """
                INSERT INTO activity_types (strava_type, display_name)
                VALUES (%s, %s)
                ON CONFLICT (strava_type) DO NOTHING;
                """,
                (
                    activity_type.strava_type,
                    activity_type.display_name,
                ),
            )

    print("Activity types seeded successfully!")