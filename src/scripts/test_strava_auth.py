from src.strava.auth import get_valid_access_token

access_token = get_valid_access_token()

print()
print("Successfully received a valid access token.")
print(f"Access token length: {len(access_token)}")