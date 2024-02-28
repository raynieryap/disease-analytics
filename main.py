import pandas as pd
import altair as alt
import requests
import os

# Define the URL of the CSV file
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

# Send a HTTP request to the URL
response = requests.get(url)

# Make sure the request was successful
assert response.status_code == 200, 'Failed to download the file'

# Write the content of the response to a file
with open('daily-covid-cases-deaths.csv', 'wb') as file:
    file.write(response.content)

# Load the data into a pandas DataFrame
df = pd.read_csv('daily-covid-cases-deaths.csv')

# Filter the data to include only the desired columns
df = df[['location', 'date', 'new_cases_smoothed']]

# Filter the data to include only the last 50 days of data
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= df['date'].max() - pd.Timedelta(days=50)]

# Filter the data to include only 10 countries
countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Russia', 'France', 'Turkey', 'Italy', 'Spain', 'Germany']
df = df[df['location'].isin(countries)]

chart = alt.Chart(df).mark_line().encode(
    x=alt.X('date', title='Date'),
    y=alt.Y('new_cases_smoothed', title='New Cases'),
    color=alt.Color('location', title='Country')
).properties(
    title='Daily New COVID-19 Cases',
    width=1000,
    height=600
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
)

# Save the chart to an HTML file
chart.save('daily-covid-cases.html')
#delete the csv file but keep the html file
os.remove('daily-covid-cases-deaths.csv')
os.remove('filtered-daily-covid-cases-deaths.csv')