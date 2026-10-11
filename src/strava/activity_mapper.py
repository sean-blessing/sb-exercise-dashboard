from datetime import datetime
from src.models.activity import Activity

def map_strava_activity(
    strava_activity: dict,
    activity_type_id: int,
) -> Activity:

    return Activity(
        strava_id=strava_activity["id"],
        activity_type_id=activity_type_id,
        name=strava_activity.get("name"),
        distance_meters=strava_activity.get("distance"),
        moving_time_seconds=strava_activity.get("moving_time"),
        elapsed_time_seconds=strava_activity.get("elapsed_time"),
        start_date=datetime.fromisoformat(
            strava_activity["start_date"].replace("Z", "+00:00")
        ),
        start_date_local=datetime.fromisoformat(
            strava_activity["start_date_local"].replace("Z", "")
        ),
        timezone=strava_activity.get("timezone"),
        elevation_gain_meters=strava_activity.get("total_elevation_gain"),
        device_name=strava_activity.get("device_name"),
        manual=strava_activity.get("manual"),
        private=strava_activity.get("private"),
        has_heartrate=strava_activity.get("has_heartrate"),
        average_heartrate=strava_activity.get("average_heartrate"),
        max_heartrate=strava_activity.get("max_heartrate"),
        created_at=None,
        updated_at=None,
    )