
from src.database.connection import get_connection
from src.database.repositories.activity_repository import ActivityRepository
from src.database.repositories.activity_type_repository import ActivityTypeRepository
from src.strava.activities import get_all_activities
from src.strava.activity_mapper import map_strava_activity


def main():
    # Step 1: Retrieve all activities from Strava.
    activities = get_all_activities()

    print()
    print(f"Retrieved {len(activities)} activities from Strava.")
    print("Starting database import...")

    # Step 2: Connect to PostgreSQL.
    with get_connection() as connection:
        activity_type_repository = ActivityTypeRepository(connection)
        activity_repository = ActivityRepository(connection)

        imported_count = 0

        # Step 3: Process each activity.
        for index, strava_activity in enumerate(activities, start=1):
            strava_type = strava_activity["type"]

            # Find the corresponding PostgreSQL activity type.
            activity_type = (
                activity_type_repository.find_by_strava_type(strava_type)
            )

            if activity_type is None:
                raise RuntimeError(
                    f"Unknown Strava activity type: {strava_type}. "
                    "Add it to activity_types before importing."
                )

            # Convert the Strava dictionary into an Activity object.
            activity = map_strava_activity(
                strava_activity,
                activity_type.activity_type_id,
            )

            # Insert the activity or update it if it already exists.
            activity_repository.save(activity)

            imported_count += 1

            # Report progress every 100 activities.
            if index % 100 == 0 or index == len(activities):
                print(f"Processed {index} of {len(activities)} activities.")

    # The database transaction commits when the connection context exits.
    print()
    print("Import completed successfully!")
    print(f"Activities processed: {imported_count}")


if __name__ == "__main__":
    main()