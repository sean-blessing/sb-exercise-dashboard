from src.models.activity_type import ActivityType

class ActivityTypeRepository:

    def __init__(self, connection):
        self.connection = connection

    def find_by_strava_type(self, strava_type: str) -> ActivityType | None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    activity_type_id,
                    strava_type,
                    display_name
                FROM activity_types
                WHERE strava_type = %s
                """,
                (strava_type,),
            )
            row = cursor.fetchone()

            if row is None:
                return None
            
            return ActivityType(
                activity_type_id=row[0],
                strava_type=row[1],
                display_name=row[2],
            )