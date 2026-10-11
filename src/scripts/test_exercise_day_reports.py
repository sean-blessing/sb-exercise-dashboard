from src.database.connection import get_connection
from src.database.repositories.activity_repository import ActivityRepository
from src.services.exercise_day_calculator import calculate_exercise_days
from src.services.exercise_day_reports import (
    compare_year_to_date,
    count_exercise_days_by_month,
    count_exercise_days_by_year,
)
from datetime import date

def main():
    # Retrieve activities from PostgreSQL.
    with get_connection() as connection:
        repository = ActivityRepository(connection)
        activity_rows = repository.find_all_with_activity_types()

    # Calculate Exercise Days.
    exercise_days = calculate_exercise_days(activity_rows)

    # Calculate yearly and monthly totals.
    yearly_counts = count_exercise_days_by_year(exercise_days)
    monthly_counts = count_exercise_days_by_month(exercise_days)

    print(f"Total Exercise Days: {len(exercise_days)}")
    print()
    print("Exercise Days by year:")

    for year, count in yearly_counts.items():
        print(f"{year}: {count}")

    print()
    print("Exercise Days by month:")

    for (year, month), count in monthly_counts.items():
        print(f"{year}-{month:02d}: {count}")

    # Compare year-to-date Exercise Days with the prior year.
    ytd_comparison = compare_year_to_date(
        exercise_days,
        reference_date=date(2026, 10, 11),
    )

    print()
    print("Year-to-date comparison:")
    print(
        f"{ytd_comparison['current_year']}: "
        f"{ytd_comparison['current_count']}"
    )
    print(
        f"{ytd_comparison['prior_year']}: "
        f"{ytd_comparison['prior_count']}"
    )
    print(f"Difference: {ytd_comparison['difference']:+d}")

if __name__ == "__main__":
    main()