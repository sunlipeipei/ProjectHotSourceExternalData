import requests
import csv
import sched
import time
from datetime import datetime
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import re

def get_weather_data(latitude, longitude):
    # Use the /points endpoint to retrieve the current grid endpoint by coordinates:
    # https://api.weather.gov/points/{latitude},{longitude}
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    
    # Make the request to the points endpoint
    response = requests.get(points_url)
    data = response.json()

    # Extract the URL for the nearest observation station
    observation_station_url = data['properties']['observationStations']
    # print(f"observation_station_url: {observation_station_url}")
    
    # Gets the list of observation stations
    stations_response = requests.get(observation_station_url)
    stations_data = stations_response.json()
    
    # Take the first station from the list
    first_station_url = stations_data['features'][0]['id']
    # print(f"first_station_url: {first_station_url}")
    
    # Gets the latest observations from the first station
    latest_observation_response = requests.get(f"{first_station_url}/observations/latest")
    latest_observation_data = latest_observation_response.json()
    
    # Gets the temperature and humidity from the latest observation
    temperature = latest_observation_data['properties']['temperature']['value']
    humidity = latest_observation_data['properties']['relativeHumidity']['value']
    
    return temperature, humidity

def get_Seattle_airquality_data(url):
    # Fetch the XML data
    response = requests.get(url)
    if response.status_code != 200:
        return "Error fetching data"
    
    # Parse the XML
    root = ET.fromstring(response.content)
    
    # Navigate to the <description> tag and extract its content
    description = root.find('.//item/description').text
    
    # Parse the HTML content inside the <description> tag
    soup = BeautifulSoup(description, 'html.parser')
    
    # Extract air quality data
    air_quality = soup.get_text(separator=' ', strip=True)
    
    # Use a regular expression to extract the AQI value and pollution type
    match = re.search(r"(\d+) AQI - Particle Pollution \(2\.5 microns\)", air_quality)
    if match:
        # Returns only the AQI value and the "Particle Pollution (2.5 microns)" part
        return f"{match.group(1)} AQI - Particle Pollution (2.5 microns)"
    else:
        return "Specific air quality data not found"

def append_to_csv(temperature, humidity, air_quality):
    # Current timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('weather_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now, temperature, humidity, air_quality])

def scheduled_weather_data(sc): 
    NEU_latitude = "47.6062"
    NEU_longitude = "-122.3321"
    Current_Conditions_RSS = "https://feeds.airnowapi.org/rss/realtime/137.xml"
    
    # Fetch weather data
    temperature, humidity = get_weather_data(NEU_latitude, NEU_longitude)
    
    # Fetch air quality data
    air_quality = get_Seattle_airquality_data(Current_Conditions_RSS)
    
    print(f"Weather Conditions at Seattle:")
    print(f"  Temperature: {temperature}°C")
    print(f"  Humidity: {humidity}%")
    print(f"  Air Quality: {air_quality}")
    append_to_csv(temperature, humidity, air_quality)
    
    # Schedule the function to be called every 3600 seconds (1 hour)
    sc.enter(3600, 1, scheduled_weather_data, (sc,))

# Scheduler instance
s = sched.scheduler(time.time, time.sleep)
# Schedule the first call to the function
s.enter(0, 1, scheduled_weather_data, (s,))
s.run()
