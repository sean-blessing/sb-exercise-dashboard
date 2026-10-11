from src.database.connection import get_connection
from src.database.repositories.activity_repository import ActivityRepository
from src.database.repositories.activity_type_repository import ActivityTypeRepository
from src.strava.activities import get_all_activities
from src.strava.activity_mapper import map_strava_activity

# Retrieve activities from Strava.

activities = get_all_activities()
strava_activity = activities[0]

# Connect to PostgreSQL and look up the activity type.

with get_connection() as connection:
    activity_type_repository = ActivityTypeRepository(connection)
    activity_repository = ActivityRepository(connection)

    strava_type = strava_activity["type"]
    activity_type = activity_type_repository.find_by_strava_type(strava_type)

    if activity_type is None:
        raise RuntimeError(f"Unknown Strava activity type: {strava_type}")

    # Convert the Strava dictionary into an Activity object.
    activity = map_strava_activity(
        strava_activity,
        activity_type.activity_type_id,
    )

    # Insert the activity, or update it if it already exists.
    activity_repository.save(activity)

    print("Activity saved successfully!")
    print(f"Strava ID: {activity.strava_id}")
    print(f"Name: {activity.name}")
    print(f"Type: {strava_type}")

