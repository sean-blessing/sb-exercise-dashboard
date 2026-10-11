from dataclasses import dataclass
from datetime import date

@dataclass
class ExerciseDay:
    exercise_date: date
    qualifying_types: list[str]
    total_distance_miles: float