
from src.database.connection import get_connection
from src.database.repositories.activity_repository import ActivityRepository
from src.database.repositories.activity_type_repository import ActivityTypeRepository
from src.strava.activities import get_all_activities
from src.strava.activity_mapper import map_strava_activity


def sync_strava_activities():
    """Fetch Strava activities and upsert them into PostgreSQL."""

    activities = get_all_activities()
    processed_count = 0

    with get_connection() as connection:
        activity_type_repository = ActivityTypeRepository(connection)
        activity_repository = ActivityRepository(connection)

        for strava_activity in activities:
            strava_type = strava_activity["type"]

            activity_type = (
                activity_type_repository.find_by_strava_type(strava_type)
            )

            if activity_type is None:
                raise RuntimeError(
                    f"Unknown Strava activity type: {strava_type}. "
                    "Add it to activity_types before syncing."
                )

            activity = map_strava_activity(
                strava_activity,
                activity_type.activity_type_id,
            )

            activity_repository.save(activity)
            processed_count += 1

    return processed_count