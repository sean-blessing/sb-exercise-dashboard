from src.strava.activities import get_all_activities
from src.strava.activity_mapper import map_strava_activity

activities = get_all_activities()
first_activity = activities[0]

activity = map_strava_activity(
    first_activity,
    activity_type_id=3,
)

print(activity)