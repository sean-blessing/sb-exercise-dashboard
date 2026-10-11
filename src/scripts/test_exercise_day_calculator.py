
from src.database.connection import get_connection
from src.database.repositories.activity_repository import ActivityRepository
from src.services.exercise_day_calculator import calculate_exercise_days


def main():
    # Retrieve activities from PostgreSQL.
    with get_connection() as connection:
        repository = ActivityRepository(connection)
        activity_rows = repository.find_all_with_activity_types()

    print(f"Activities retrieved: {len(activity_rows)}")

    # Calculate Exercise Days.
    exercise_days = calculate_exercise_days(activity_rows)

    print(f"Exercise Days found: {len(exercise_days)}")
    print()

    # Display the 10 most recent Exercise Days.
    print("Most recent Exercise Days:")

    for exercise_day in exercise_days[-10:][::-1]:
        qualifying_types = ", ".join(exercise_day.qualifying_types)

        print(
            f"{exercise_day.exercise_date} | "
            f"{qualifying_types} | "
            f"{exercise_day.total_distance_miles:.2f} miles"
        )


if __name__ == "__main__":
    main()