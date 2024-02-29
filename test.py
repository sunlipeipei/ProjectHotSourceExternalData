<<<<<<< HEAD
    # Extract air quality data
    air_quality = soup.get_text(separator=' ', strip=True)
    
    # Use a regular expression to extract the AQI value and pollution type
    match = re.search(r"(\d+) AQI - Particle Pollution \(2\.5 microns\)", air_quality)
    if match:
        # Returns only the AQI value and the "Particle Pollution (2.5 microns)" part
        return f"{match.group(1)} AQI - Particle Pollution (2.5 microns)"
    else:
        return "Specific air quality data not found"