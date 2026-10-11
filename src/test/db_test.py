import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

with psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
) as connection:

    print("PostgreSQL connection successful!")

    with connection.cursor() as cursor:

        cursor.execute("SELECT version();")

        result = cursor.fetchone()

        print(f"PostgreSQL version: {result[0]}")