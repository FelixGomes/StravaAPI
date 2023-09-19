import matplotlib.pyplot as plt


def create_visualization(average_speed_converted):
    # Create a bar plot to visualize the average velocity by year
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

    average_velocity_by_year = average_speed_converted
    average_velocity_by_year.plot(kind="bar", color="skyblue")

    plt.title("Average Speed by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Speed (km/h)")  # You can adjust the ylabel as needed
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()
