from dataclasses import dataclass
from datetime import datetime


@dataclass
class Activity:
    strava_id: int
    activity_type_id: int
    name: str | None
    distance_meters: float | None
    moving_time_seconds: int | None
    elapsed_time_seconds: int | None
    start_date: datetime | None
    start_date_local: datetime | None
    timezone: str | None
    elevation_gain_meters: float | None
    device_name: str | None
    manual: bool | None
    private: bool | None
    has_heartrate: bool | None
    average_heartrate: float | None
    max_heartrate: float | None
    created_at: datetime | None
    updated_at: datetime | Nonecd 