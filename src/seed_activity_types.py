import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

activity_types = [
    ("Walk", "Walk"),
    ("Run", "Run"),
    ("Ride", "Ride"),
    ("Hike", "Hike"),
    ("Workout", "Workout"),
    ("WeightTraining", "Weight Training"),
    ("AlpineSki", "Alpine Ski"),
    ("Elliptical", "Elliptical"),
    ("EBikeRide", "E-Bike Ride"),
    ("Yoga", "Yoga"),
    ("Canoeing", "Canoeing"),
]

with psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
) as connection:

    with connection.cursor() as cursor:

        for strava_type, display_name in activity_types:

            cursor.execute(
                """
                INSERT INTO activity_types (strava_type, display_name)
                VALUES (%s, %s)
                ON CONFLICT (strava_type) DO NOTHING;
                """,
                (strava_type, display_name),
            )

    print("Activity types seeded successfully!")