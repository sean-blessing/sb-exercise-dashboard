from src.services.exercise_dashboard_service import get_exercise_dashboard_data

def main():
    dashboard_data = get_exercise_dashboard_data()

    print("Exercise Dashboard Summary")
    print("==========================")
    print(f"Activities: {dashboard_data['activity_count']}")
    print(f"Exercise Days: {dashboard_data['exercise_day_count']}")

    comparison = dashboard_data["ytd_comparison"]

    print()
    print("Year-to-date comparison:")
    print(
        f"{comparison['current_year']}: "
        f"{comparison['current_count']}"
    )
    print(
        f"{comparison['prior_year']}: "
        f"{comparison['prior_count']}"
    )
    print(f"Difference: {comparison['difference']:+d}")

    print()
    print("Exercise Days by year:")

    for year, count in dashboard_data["yearly_counts"].items():
        print(f"{year}: {count}")

if __name__ == "__main__":
    main()