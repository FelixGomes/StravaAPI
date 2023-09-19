import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from pandas import json_normalize
from tqdm import tqdm
import time
import random
import save_json
import data_viz

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/activities"

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

print("Requesting pages (200 activities per full page)...")
activities_df = pd.DataFrame()
page = 1
page_non_empty = True

# Retrieve all of your data and download it to the dataframe
while page_non_empty:
    header = {"Authorization": "Bearer " + access_token}
    param = {"per_page": 200, "page": page}
    my_activities = requests.get(activites_url, headers=header, params=param).json()
    activities_df = activities_df._append(my_activities, ignore_index=True)
    page_non_empty = bool(my_activities)
    print(page)
    page += 1

print("\n", len(activities_df), "activities downloaded")

# activities_df = json_normalize(activities_df)
print(activities_df.columns)  # See a list of all columns in the table
# print(activities_df.shape)  # See the dimensions of the table.

# Create new dataframe with only columns I care about
cols = [
    "name",
    "type",
    "distance",
    "moving_time",
    "elapsed_time",
    "average_speed",
    "max_speed",
    "total_elevation_gain",
    "start_date_local",
    "average_watts",
    "kilojoules",
]
# Create a new DataFrame by copying the selected columns from activities_df
activities = activities_df[cols].copy()

# Convert the "start_date_local" column to datetime
activities["start_date_local"] = pd.to_datetime(activities["start_date_local"])

# Extract "start_time" and "start_date_local" columns
activities["start_date_local"] = activities["start_date_local"].dt.date

# Display the first 5 rows
print(activities.head(5))

bike_rides = activities.loc[activities["type"] == "Ride"]
# Extract the year and create a new column called 'year'
bike_rides["start_date_local"] = pd.to_datetime(
    bike_rides["start_date_local"], format="%Y-%m-%d"
)
bike_rides["year"] = bike_rides["start_date_local"].dt.year

# convert to km/h
average_speed_converted = bike_rides.groupby("year")["average_speed"].mean() * 3.6

data_viz.create_visualization(average_speed_converted)

save_json.convert_df_to_json(bike_rides)
