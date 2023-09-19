def convert_df_to_json(bike_rides):
    json_data = bike_rides.to_json(orient="records")

    # Save JSON data to a file
    with open("bike_rides.json", "w") as json_file:
        json_file.write(json_data)

    return print("JSON data saved to bike_rides.json")
