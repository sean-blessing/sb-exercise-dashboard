from dataclasses import dataclass

@dataclass
class ActivityType:
    activity_type_id: int | None
    strava_type: str
    display_name: str