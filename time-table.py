# import the necessary packages
import pandas as pd
from tabulate import tabulate
import datetime

# Read the CSV files
data = pd.read_csv('schedule.csv')
venues_data = pd.read_csv('venues.csv')

# Define venues with their capacities
venues = dict(zip(venues_data['Venues'], venues_data['Capacity']))

# Define the columns for the time table schedule table.
table_data = pd.DataFrame(columns=['Days', 'Courses', 'Start-Time', 'End-Time', 'Venues', "Student's population"], dtype=object)

# Add columns to the table
table_headers = table_data.columns.tolist()

# Define a function to find an available time slot within the given venue
def find_available_slot(days, start_time, end_time, venue):
    # Find an available time slot within the given venue
    for index, existing_row in table_data.iterrows():
        # Check if the time slot is already occupied by another course
        if (
            days == existing_row['Days']  # Check if the days overlap with an existing scheduled course
            and start_time < existing_row['End-Time']  # Check if the start time is earlier than the end time of an existing course
            and end_time > existing_row['Start-Time']  # Check if the end time is later than the start time of an existing course
            and venue == existing_row['Venues']  # Check if the venue is the same as the existing course
        ):
            return False  # Return False if the time slot is not available
    return True  # Return True if the time slot is available

# Define a function to find an available venue for the given course and schedule
def find_available_venue(days, courses, start_time, end_time, students_population):
    # Convert start_time and end_time to datetime.time objects
    start_time = datetime.datetime.strptime(start_time, '%I:%M %p').time()  # Convert the start time to a datetime.time object
    end_time = datetime.datetime.strptime(end_time, '%I:%M %p').time()  # Convert the end time to a datetime.time object

    # Find an available venue that has enough capacity for the given course and schedule
    for venue, venue_capacity in venues.items():
        # Check if the venue has enough capacity for the given course and schedule
        if venue_capacity >= students_population:  # Compare the venue capacity with the student population
            is_slot_available = find_available_slot(days, start_time, end_time, venue)  # Check if an available time slot exists within the venue
            if is_slot_available:
                # Add the course to the table if the time slot is available
                table_data.loc[len(table_data)] = [days, courses, start_time, end_time, venue, students_population]  # Add the course details to the table_data DataFrame
                return venue  # Return the venue if the course is added to the table
    return None  # Return None if no available venue is found for the course and schedule

# Process each row in the data
for index, row in data.iterrows():
    days = row['Days']  # Retrieve the value of the 'Days' column from the current row
    courses = row['Courses']  # Retrieve the value of the 'Courses' column from the current row
    start_time = row['Start-Time']  # Retrieve the value of the 'Start-Time' column from the current row
    end_time = row['End-Time']  # Retrieve the value of the 'End-Time' column from the current row
    students_population = row["Students population"]  # Retrieve the value of the 'Students population' column from the current row

    # Find an available venue for the course
    venue = find_available_venue(days, courses, start_time, end_time, students_population)  # Call the find_available_venue function to find a suitable venue for the course

    if venue is None:  # Check if no venue is available for the course
        # If no venue is available, try to find an alternative time slot within the same venue
        for index, existing_row in table_data.iterrows():
            if (
                days == existing_row['Days']  # Check if the days overlap with an existing scheduled course
                and start_time < existing_row['End-Time']  # Check if the start time is earlier than the end time of an existing course
                and end_time > existing_row['Start-Time']  # Check if the end time is later than the start time of an existing course
            ):
                # Generate a new start_time and end_time for the alternative time slot
                start_time                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 = existing_row['End-Time']  # Set the start time as the end time of the existing course
                end_time = start_time + (end_time - start_time)  # Calculate the new end time by adding the duration of the course
                venue = existing_row['Venues']  # Assign the same venue as the existing course

                # Find an available time slot within the same venue
                if find_available_slot(days, start_time, end_time, venue):  # Call the find_available_slot function to check if the new time slot is available
                    table_data.loc[len(table_data)] = [days, courses, start_time, end_time, venue, students_population]  # Add the course to the table_data DataFrame
                    break  # Exit the loop after finding an alternative time slot or trying all existing courses

# Format the table data
formatted_table_data = []  # Create an empty list to store the formatted table data
for index, row in table_data.iterrows():  # Iterate over each row in the table data
    start_time = row['Start-Time'].strftime('%I:%M %p')  # Format the start time using '%I:%M %p' format (e.g., 09:00 AM)
    end_time = row['End-Time'].strftime('%I:%M %p')  # Format the end time using '%I:%M %p' format (e.g., 10:30 AM)
    formatted_table_data.append([row['Days'], row['Courses'], start_time, end_time, row['Venues'], row["Student's population"]])  # Append the formatted row to the formatted table data list

# Check if the table is empty
if data.empty:
    print("No examination time table schedule found!")  # Print a message indicating that there is no examination time table schedule
else:
    # Print the table
    table = tabulate(formatted_table_data, headers=table_headers, tablefmt='fancy_grid')  # Generate the formatted table using the formatted table data
    print(table)  # Print the formatted table
