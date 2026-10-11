from src.models.activity import Activity

class ActivityRepository:

    def __init__(self, connection):
        self.connection = connection

    def save(self, activity: Activity) -> None:
        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO activities (
                    strava_id,
                    activity_type_id,
                    name,
                    distance_meters,
                    moving_time_seconds,
                    elapsed_time_seconds,
                    start_date,
                    start_date_local,
                    timezone,
                    elevation_gain_meters,
                    device_name,
                    manual,
                    private,
                    has_heartrate,
                    average_heartrate,
                    max_heartrate
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (strava_id) DO UPDATE SET
                    activity_type_id = EXCLUDED.activity_type_id,
                    name = EXCLUDED.name,
                    distance_meters = EXCLUDED.distance_meters,
                    moving_time_seconds = EXCLUDED.moving_time_seconds,
                    elapsed_time_seconds = EXCLUDED.elapsed_time_seconds,
                    start_date = EXCLUDED.start_date,
                    start_date_local = EXCLUDED.start_date_local,
                    timezone = EXCLUDED.timezone,
                    elevation_gain_meters = EXCLUDED.elevation_gain_meters,
                    device_name = EXCLUDED.device_name,
                    manual = EXCLUDED.manual,
                    private = EXCLUDED.private,
                    has_heartrate = EXCLUDED.has_heartrate,
                    average_heartrate = EXCLUDED.average_heartrate,
                    max_heartrate = EXCLUDED.max_heartrate,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    activity.strava_id,
                    activity.activity_type_id,
                    activity.name,
                    activity.distance_meters,
                    activity.moving_time_seconds,
                    activity.elapsed_time_seconds,
                    activity.start_date,
                    activity.start_date_local,
                    activity.timezone,
                    activity.elevation_gain_meters,
                    activity.device_name,
                    activity.manual,
                    activity.private,
                    activity.has_heartrate,
                    activity.average_heartrate,
                    activity.max_heartrate,
                ),
            )
    
    def find_all_with_activity_types(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    a.strava_id,
                    a.activity_type_id,
                    a.name,
                    a.distance_meters,
                    a.moving_time_seconds,
                    a.elapsed_time_seconds,
                    a.start_date,
                    a.start_date_local,
                    a.timezone,
                    a.elevation_gain_meters,
                    a.device_name,
                    a.manual,
                    a.private,
                    a.has_heartrate,
                    a.average_heartrate,
                    a.max_heartrate,
                    a.created_at,
                    a.updated_at,
                    at.strava_type
                FROM activities a
                JOIN activity_types at
                    ON a.activity_type_id = at.activity_type_id
                ORDER BY a.start_date_local
                """
            )
            rows = cursor.fetchall()

        return rows