def convert_df_to_json(bike_rides, json):
    json_data = bike_rides.to_json(orient="records")

    # Save JSON data to a file
    with open(json, "w") as json_file:
        json_file.write(json_data)

    return print(f"JSON data saved to {json}")
