from src.database.connection import get_connection
from src.database.repositories.activity_type_repository import ActivityTypeRepository

with get_connection() as connection:
    repository = ActivityTypeRepository(connection)
    for strava_type in ["Walk", "Run", "Ride", "Hike"]:
        activity_type = repository.find_by_strava_type(strava_type)

        if activity_type is None:
            print(f"Type not found: {strava_type}")
        else:
            print(
                f"{activity_type.strava_type}: "
                f"ID = {activity_type.activity_type_id}"
            )
