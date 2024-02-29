import requests

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

# Based on Northeastern 225 Terry Ave N latitude and longitude
NEU_latitude = "47.6062"
NEU_longitude = "-122.3321"
temperature, humidity = get_weather_data(NEU_latitude, NEU_longitude)
print(f"Temperature: {temperature}C, Humidity: {humidity}%")
