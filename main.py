import pandas as pd
import altair as alt
import requests
import os

def download_covid_data():
    """
    Downloads the daily COVID-19 cases and deaths data from a URL,
    saves it to a CSV file, and returns the data as a pandas DataFrame.

    Returns:
    df (pandas.DataFrame): DataFrame containing the daily COVID-19 cases and deaths data.
    """
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

    return df

def filter_covid_data(df):
    """
    Filters the COVID-19 cases and deaths data to include only the desired columns,
    the last 50 days of data, and data for 10 specific countries.

    Args:
    df (pandas.DataFrame): DataFrame containing the daily COVID-19 cases and deaths data.

    Returns:
    df (pandas.DataFrame): Filtered DataFrame containing the desired COVID-19 data.
    """
    # Filter the data to include only the desired columns
    df = df[['location', 'date', 'new_cases_smoothed']]

    # Filter the data to include only the last 50 days of data
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= df['date'].max() - pd.Timedelta(days=50)]

    # Filter the data to include only 10 countries
    countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Russia', 'France', 'Turkey', 'Italy', 'Spain', 'Germany']
    df = df[df['location'].isin(countries)]

    return df

def create_chart(df):
    """
    Creates an Altair line chart based on the filtered COVID-19 data.

    Args:
    df (pandas.DataFrame): Filtered DataFrame containing the desired COVID-19 data.

    Returns:
    chart (altair.Chart): Altair line chart representing the daily new COVID-19 cases.
    """
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

    return chart

def save_chart(chart):
    """
    Saves the Altair chart as an HTML file.

    Args:
    chart (altair.Chart): Altair line chart representing the daily new COVID-19 cases.
    """
    # Save the chart to an HTML file
    chart.save('daily-covid-cases.html')

def delete_csv_file():
    """
    Deletes the CSV file containing the daily COVID-19 cases and deaths data.
    """
    os.remove('daily-covid-cases-deaths.csv')

# Download the COVID-19 data
df = download_covid_data()

# Filter the COVID-19 data
df = filter_covid_data(df)

# Create the chart
chart = create_chart(df)

# Save the chart as an HTML file
save_chart(chart)

# Delete the CSV file
delete_csv_file()
