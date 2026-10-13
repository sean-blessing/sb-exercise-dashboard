
from datetime import date
from collections import defaultdict
from src.database.connection import get_connection
from src.database.repositories.activity_repository import ActivityRepository
from src.services.exercise_day_calculator import calculate_exercise_days
from src.services.exercise_day_reports import (
    compare_year_to_date,
    count_exercise_days_by_month,
    count_exercise_days_by_year,
)


def get_exercise_dashboard_data(reference_date=None):
    """
    Retrieve activities and build the data needed by the dashboard.

    reference_date defaults to today's date and can be supplied
    explicitly when testing historical reports.
    """
    if reference_date is None:
        reference_date = date.today()

    # Retrieve the activities from PostgreSQL.
    with get_connection() as connection:
        repository = ActivityRepository(connection)
        activity_rows = repository.find_all_with_activity_types()

    # Calculate qualifying Exercise Days.
    exercise_days = calculate_exercise_days(activity_rows)

    # Build the reports.
    yearly_counts = count_exercise_days_by_year(exercise_days)
    monthly_counts = count_exercise_days_by_month(exercise_days)
    ytd_comparison = compare_year_to_date(
        exercise_days,
        reference_date,
    )
    
    current_month_miles = defaultdict(float)

    for row in activity_rows:
        start_date_local = row[7]
        distance_meters = row[3]
        activity_type = row[18]

        if start_date_local is None or distance_meters is None:
            continue

        activity_date = start_date_local.date()

        if (
            activity_date.year == reference_date.year
            and activity_date.month == reference_date.month
        ):
            current_month_miles[activity_type] += (
                distance_meters / 1609.344
            )

    # Return everything the dashboard needs.
    return {
        "activity_count": len(activity_rows),
        "exercise_days": exercise_days,
        "exercise_day_count": len(exercise_days),
        "yearly_counts": yearly_counts,
        "monthly_counts": monthly_counts,
        "ytd_comparison": ytd_comparison,
        "reference_date": reference_date,
        "current_month_miles": dict(sorted(current_month_miles.items())),
    }