import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def activities_url():
    return "https://www.strava.com/api/v3/activities"


def token():
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": "xxx",
        "client_secret": "xxx",
        "refresh_token": "xxx",
        "grant_type": "refresh_token",
        "f": "json",
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()["access_token"]
    print("Access Token = {}\n".format(access_token))
    return access_token
