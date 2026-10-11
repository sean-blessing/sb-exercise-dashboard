from collections import Counter
from datetime import date

def count_exercise_days_by_year(exercise_days):
    """
    Return the number of Exercise Days for each calendar year.

    Example result:
        {2024: 142, 2025: 156, 2026: 98}
    """
    counts = Counter()

    for exercise_day in exercise_days:
        year = exercise_day.exercise_date.year
        counts[year] += 1

    return dict(sorted(counts.items()))

def count_exercise_days_by_month(exercise_days):
    """
    Return the number of Exercise Days for each calendar month.

    Example result:
        {
            (2025, 1): 12,
            (2025, 2): 10,
            (2025, 3): 14,
        }
    """
    counts = Counter()

    for exercise_day in exercise_days:
        year = exercise_day.exercise_date.year
        month = exercise_day.exercise_date.month
        counts[(year, month)] += 1

    return dict(sorted(counts.items()))

def compare_year_to_date(exercise_days, reference_date):
    """
    Compare Exercise Days through reference_date with the same
    calendar period in the previous year.

    Returns a dictionary containing current-year and prior-year totals.
    """
    current_year = reference_date.year
    prior_year = current_year - 1

    current_count = 0
    prior_count = 0

    for exercise_day in exercise_days:
        exercise_date = exercise_day.exercise_date

        if exercise_date.year == current_year:
            if exercise_date <= reference_date:
                current_count += 1

        elif exercise_date.year == prior_year:
            # Use the same month/day in the previous year.
            try:
                prior_cutoff = reference_date.replace(year=prior_year)
            except ValueError:
                # Handles February 29 when the prior year isn't a leap year.
                prior_cutoff = date(prior_year, 2, 28)

            if exercise_date <= prior_cutoff:
                prior_count += 1

    return {
        "current_year": current_year,
        "current_count": current_count,
        "prior_year": prior_year,
        "prior_count": prior_count,
        "difference": current_count - prior_count,
    }