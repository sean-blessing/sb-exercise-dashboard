import os

import requests
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("STRAVA_ACCESS_TOKEN")

url = "https://www.strava.com/api/v3/athlete/activities"

headers = {
    "Authorization": f"Bearer {access_token}"
}

all_activities = []
page = 1
per_page = 100

while True:
    print(f"Requesting page {page}...")

    params = {
        "page": page,
        "per_page": per_page
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print(f"API request failed: {response.status_code}")
        print(response.text)
        break

    activities = response.json()

    if not activities:
        break

    all_activities.extend(activities)

    print(f"  Retrieved {len(activities)} activities.")

    if len(activities) < per_page:
        break

    page += 1

print()
print("Fields returned by Strava:")
print("-" * 50)

first_activity = all_activities[0]

for field, value in first_activity.items():
    print(f"{field:25} {type(value).__name__:15} {value}")

from collections import Counter

print()
print("Activity types:")
print("-" * 40)

type_counts = Counter(
    activity["type"]
    for activity in all_activities
)

for activity_type, count in type_counts.most_common():
    print(f"{activity_type:25} {count}")


print()
print("Sport types:")
print("-" * 40)

sport_type_counts = Counter(
    activity["sport_type"]
    for activity in all_activities
)

for sport_type, count in sport_type_counts.most_common():
    print(f"{sport_type:25} {count}")