import pandas as pd
import altair as alt
from datetime import datetime

# Read the influenza data from a CSV file
influenza_data = pd.read_csv('filtered_influenza.csv')

# Prompt the user to input the country
country = input("Enter the country: ").title().strip()

# Check if the user inputted more than one country
if ',' in country:
    print("Error: Please enter only one country.")
    exit(1)

# Check if country exists in the data
if country not in influenza_data['Country'].unique():
    print(f"Error: {country} is not available in the data.")
    exit(1)

# Convert the 'Date' column to datetime
influenza_data['Date'] = pd.to_datetime(influenza_data['Date'])

# Prompt the user to input the start date and end date
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Convert the input strings to datetime objects
start_date = datetime.strptime(start_date, '%Y-%m-%d')
end_date = datetime.strptime(end_date, '%Y-%m-%d')

# Check that the start date is not after the end date
if start_date > end_date:
    print("Error: The start date can't be after the end date.")
    exit(1)

# Filter the data for the selected country and date range
filtered_data = influenza_data[influenza_data['Country'] == country]
filtered_data = filtered_data[(filtered_data['Date'] >= start_date) & (filtered_data['Date'] <= end_date)]

# Prepare the data for cases and deaths
cases_data = filtered_data.copy()
cases_data['Type'] = 'Cases'
deaths_data = filtered_data.copy()
deaths_data['Type'] = 'Deaths'
deaths_data['Cases'] = deaths_data['Deaths']  # Use the 'Deaths' column for the 'Cases' value
combined_data = pd.concat([cases_data, deaths_data])

# Create a layered bar chart using Altair
chart = alt.Chart(combined_data).mark_bar().encode(
    x='Date:T',
    y='Cases:Q',
    color='Type:N',  # Use the 'Type' column for the color encoding
    tooltip=['Country', 'Date', 'Cases', 'Type']
).properties(
    title=f'{country} Cases & Deaths to Influenza'  # Use f-string formatting to include the country name in the title
)

# Save the chart to an HTML file
chart.save('influenza-cases-deaths-bar.html')
