import requests
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import re

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

Current_Conditions_RSS = "https://feeds.airnowapi.org/rss/realtime/137.xml"
air_quality = get_Seattle_airquality_data(Current_Conditions_RSS)
print(f"Air quality: {air_quality}")
