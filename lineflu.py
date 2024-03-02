import pandas as pd
import altair as alt
from datetime import datetime

try:
    # Load the influenza data from CSV
    influenza_data = pd.read_csv('filtered_influenza.csv')
except FileNotFoundError:
    print("Error: File not found.")
    exit(1)
except pd.errors.ParserError:
    print("Error: Unable to read the file.")
    exit(1)

# Convert the 'Date' column to datetime format
influenza_data['Date'] = pd.to_datetime(influenza_data['Date'])

# Ask the user to input the countries, start date, and end date
countries = input("Enter the countries (comma-separated): ").title().split(',')
# Strip the white spaces from the countries if there are any
countries = [country.strip() for country in countries]

# Check if the input countries are available in the data
for country in countries:
    if country not in influenza_data['Country'].unique():
        print(f"Error: {country} is not available in the data.")
        exit(1)

# Ask the user to input the start date and end date
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Convert the input strings to datetime objects
start_date = datetime.strptime(start_date, '%Y-%m-%d')
end_date = datetime.strptime(end_date, '%Y-%m-%d')

# Check that the start date is not after the end date
if start_date > end_date:
    print("Error: The start date can't be after the end date.")
    exit(1)

# Filter the data based on the selected countries and date range
filtered_data = influenza_data[influenza_data['Country'].isin(countries)]
filtered_data = filtered_data[(filtered_data['Date'] >= start_date) & (filtered_data['Date'] <= end_date)]

# Create the line chart using Altair
chart = alt.Chart(filtered_data).mark_line().encode(
    x='Date:T',
    y='Cases:Q',
    color='Country:N'
).properties(
    title='Influenza Cases'
)

# Save the chart as an HTML file
chart.save('influenza-cases-line.html')
