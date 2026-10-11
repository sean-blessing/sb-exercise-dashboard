import pandas as pd
import streamlit as st

from src.services.exercise_dashboard_service import get_exercise_dashboard_data
from src.services.strava_sync_service import sync_strava_activities

st.set_page_config(
    page_title="SB Exercise Dashboard",
    page_icon="🚴",
    layout="wide",
)

st.title("SB Exercise Dashboard")
st.caption("Your personal exercise history")

if st.button("Sync Now", type="primary"):
    try:
        with st.spinner("Syncing activities from Strava..."):
            processed_count = sync_strava_activities()

        st.success(
            f"Sync completed! Processed {processed_count:,} activities."
        )

        st.rerun()

    except Exception as error:
        st.error(f"Sync failed: {error}")

with st.spinner("Loading exercise data..."):
    dashboard_data = get_exercise_dashboard_data()

st.subheader("Overall Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Activities",
        value=f"{dashboard_data['activity_count']:,}",
    )

with col2:
    st.metric(
        label="Exercise Days",
        value=f"{dashboard_data['exercise_day_count']:,}",
    )

with col3:
    ytd = dashboard_data["ytd_comparison"]
    st.metric(
        label=f"Exercise Days in {ytd['current_year']}",
        value=ytd["current_count"],
        delta=f"{ytd['difference']:+,} vs. {ytd['prior_year']} YTD",
    )

st.divider()

st.subheader("Exercise Days by Year")

yearly_counts = dashboard_data["yearly_counts"]

yearly_chart_data = pd.DataFrame(
    {
        "Year": list(yearly_counts.keys()),
        "Exercise Days": list(yearly_counts.values()),
    }
).set_index("Year")

st.bar_chart(yearly_chart_data)

st.divider()

st.subheader("Exercise Days by Month")

monthly_counts = dashboard_data["monthly_counts"]
available_years = sorted(
    {year for year, month in monthly_counts},
    reverse=True,
)

selected_year = st.selectbox(
    "Select year",
    available_years,
)

monthly_chart_data = pd.DataFrame(
    [
        {
            "Month": f"{year}-{month:02d}",
            "Exercise Days": count,
        }
        for (year, month), count in monthly_counts.items()
        if year == selected_year
    ]
).set_index("Month")

st.bar_chart(monthly_chart_data)

st.divider()

st.subheader("Year-to-Date Comparison")

ytd = dashboard_data["ytd_comparison"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label=f"{ytd['current_year']} Exercise Days",
        value=ytd["current_count"],
    )

with col2:
    st.metric(
        label=f"{ytd['prior_year']} Exercise Days (same date range)",
        value=ytd["prior_count"],
    )

with col3:
    st.metric(
        label="Difference",
        value=f"{ytd['difference']:+,}",
        delta="vs. last year",
    )