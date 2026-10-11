import os
import webbrowser
import requests
import time
from urllib.parse import urlencode

from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

client_id = os.getenv("STRAVA_CLIENT_ID")
client_secret = os.getenv("STRAVA_CLIENT_SECRET")

app = Flask(__name__)

def get_valid_access_token():
    expires_at = int(os.getenv("STRAVA_TOKEN_EXPIRES_AT", "0"))

    current_time = int(time.time())

    if current_time < expires_at:
        return os.getenv("STRAVA_ACCESS_TOKEN")

    return refresh_access_token()

def refresh_access_token():
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
            "grant_type": "refresh_token",
        },
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Strava token refresh failed: "
            f"{response.status_code} - {response.text}"
        )

    token_data = response.json()

    new_access_token = token_data["access_token"]
    new_refresh_token = token_data["refresh_token"]
    expires_at = token_data["expires_at"]

    with open(".env", "r") as env_file:
        env_contents = env_file.read()

    lines = []

    for line in env_contents.splitlines():
        if line.startswith("STRAVA_ACCESS_TOKEN="):
            lines.append(f"STRAVA_ACCESS_TOKEN={new_access_token}")
        elif line.startswith("STRAVA_REFRESH_TOKEN="):
            lines.append(f"STRAVA_REFRESH_TOKEN={new_refresh_token}")
        elif line.startswith("STRAVA_TOKEN_EXPIRES_AT="):
            lines.append(f"STRAVA_TOKEN_EXPIRES_AT={expires_at}")
        else:
            lines.append(line)

    if not any(
        line.startswith("STRAVA_TOKEN_EXPIRES_AT=")
        for line in lines
    ):
        lines.append(f"STRAVA_TOKEN_EXPIRES_AT={expires_at}")

    with open(".env", "w") as env_file:
        env_file.write("\n".join(lines) + "\n")

    print("Strava access token refreshed.")

    return new_access_token

@app.route("/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        return f"Authorization failed: {error}"

    if not code:
        return "No authorization code received."

    print(f"Authorization code received.")

    token_response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
        },
    )

    if token_response.status_code != 200:
        print("Token exchange failed.")
        print(token_response.text)
        return "Token exchange failed. Check the VS Code terminal."

    token_data = token_response.json()

    print("Token exchange successful!")
    print(f"Athlete ID: {token_data['athlete']['id']}")
    print(f"Access token received.")
    print(f"Refresh token received.")

    with open(".env", "a") as env_file:
        env_file.write(f"\nSTRAVA_ACCESS_TOKEN={token_data['access_token']}")
        env_file.write(f"\nSTRAVA_REFRESH_TOKEN={token_data['refresh_token']}")

    return "Authorization and token exchange successful! You can close this browser window."


if __name__ == "__main__":
    # Build the Strava authorization URL
    authorization_url = "https://www.strava.com/oauth/authorize"

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:5000/callback",
        "approval_prompt": "auto",
        "scope": "activity:read_all",
    }

    url = authorization_url + "?" + urlencode(params)

    print("Opening Strava authorization page...")
    webbrowser.open(url)

    print("Starting local callback server...")
    app.run(port=5000)