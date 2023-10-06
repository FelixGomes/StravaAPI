import requests
import pandas as pd
import save_json, request_access
import time
from pandas import json_normalize

activities_url = request_access.activities_url()
access_token = request_access.token()


def fetch_activities(access_token, page):
    header = {"Authorization": "Bearer " + access_token}
    param = {"per_page": 200, "page": page}
    my_activities = requests.get(activities_url, headers=header, params=param)

    if my_activities.status_code == 200:
        return my_activities.json()
    else:
        return print(
            f"Fail! Response HTTP: {my_activities.status_code} {my_activities.reason}"
        )


def fetch_detailed_activities(activities_detailed_df, activity_ids, access_token):
    for id in activity_ids:
        header = {"Authorization": "Bearer " + access_token}
        http_get_activity = (
            f"https://www.strava.com/api/v3/activities/{id}?include_all_efforts=true"
        )

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            response = requests.get(http_get_activity, headers=header)
            counter_15min = response.headers["X-RateLimit-Usage"].split(",")[0]
            counter_daily = response.headers["X-RateLimit-Usage"].split(",")[1]

            if response.status_code == 429:
                print("Rate limit reached. Retrying in 15 minutes...")
                time.sleep(920)  # Sleep for 15 minutes
                retry_count += 1

            elif response.status_code == 200:
                print(
                    f"15 min requests: {counter_15min}/200 and daily requests: {counter_daily}/2000"
                )
                activities_detailed_df = activities_detailed_df._append(
                    response.json(), ignore_index=True
                )
                break

            else:
                print(f"Fail! Response HTTP: {response.status_code} {response.reason}")
                break

    return activities_detailed_df


def main():
    print("Requesting pages (200 activities per full page)...")
    activities_detailed_df = pd.DataFrame()
    page = 1
    page_not_empty = True

    try:
        while page_not_empty:
            my_activities = fetch_activities(access_token, page)

            if my_activities is not None:
                # Extract activity IDs from the current page
                activity_ids = [str(activity["id"]) for activity in my_activities]

                # Fetch detailed information for the current batch of activities
                activities_detailed_df = fetch_detailed_activities(
                    activities_detailed_df, activity_ids, access_token
                )

                # save progress
                save_json.convert_df_to_json(
                    activities_detailed_df, "bike_rides_detailed.json"
                )

                page_not_empty = bool(my_activities)
                print(
                    f"Page:{page} - Processed:{len(activities_detailed_df)} detailed activities."
                )
            else:
                print(f"Failed to fetch activities for page {page}")
                break

            page += 1

    except Exception as e:
        print("Error:", str(e))
        if not activities_detailed_df.empty:
            save_json.convert_df_to_json(
                activities_detailed_df, "bike_rides_detailed.json"
            )


# initialize the code
if __name__ == "__main__":
    main()
