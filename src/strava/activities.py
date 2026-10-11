import requests

from src.strava.auth import get_valid_access_token

def get_all_activities():
    access_token = get_valid_access_token()
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
            raise RuntimeError(
                f"Strava API request failed: "
                f"{response.status_code} - {response.text}"
            )

        activities = response.json()

        if not activities:
            break

        all_activities.extend(activities)

        print(f"  Retrieved {len(activities)} activities.")

        if len(activities) < per_page:
            break

        page += 1

    return all_activities