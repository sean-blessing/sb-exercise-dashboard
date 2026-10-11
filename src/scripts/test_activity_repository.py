from datetime import datetime, timezone

from src.database.connection import get_connection
from src.database.repositories.activity_repository import ActivityRepository
from src.models.activity import Activity

test_activity = Activity(
    strava_id=99999999999,
    activity_type_id=3,
    name="Repository Test Ride - UPD",
    distance_meters=10000.0,
    moving_time_seconds=1800,
    elapsed_time_seconds=1900,
    start_date=datetime.now(timezone.utc),
    start_date_local=datetime.now(),
    timezone="(GMT-05:00) America/New_York",
    elevation_gain_meters=100.0,
    device_name="Test Device",
    manual=False,
    private=False,
    has_heartrate=True,
    average_heartrate=120.0,
    max_heartrate=145.0,
    created_at=None,
    updated_at=None,
)

with get_connection() as connection:
    repository = ActivityRepository(connection)
    repository.save(test_activity)
    print("Activity saved successfully!")