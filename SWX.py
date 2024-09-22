#!/usr/bin/env python3
#created by chengmania, KC3SMW, for free use, on a Tuesday in September 2024


import requests
import xml.etree.ElementTree as ET

# URL of the XML feed
url = "https://www.hamqsl.com/solarxml.php"

# Mapping XML tags to more human-readable titles
tag_mapping = {
    "updated": "Last Updated",
    "solarflux": "Solar Flux",
    "aindex": "A-Index",
    "kindex": "K-Index",
    "kindexnt": "K-Index (Non-Telemetered)",
    "xray": "X-Ray Level",
    "sunspots": "Sunspot Count",
    "heliumline": "Helium Line",
    "protonflux": "Proton Flux",
    "electronflux": "Electron Flux",
    "aurora": "Aurora Level",
    "normalization": "Normalization Factor",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "solarwind": "Solar Wind Speed",
    "magneticfield": "Magnetic Field Strength",
    "geomagfield": "Geomagnetic Field",
    "signalnoise": "Signal Noise Level",
    "fof2": "Critical Frequency foF2",
    "muf": "Maximum Usable Frequency"
}

# Fetch the XML data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML data
    root = ET.fromstring(response.content)

    # Display general information about the XML feed
    print("Solar Activity Information\n" + "="*30)

    # Iterate over elements, find human-readable title, and print the values
    for elem in root.iter():
        if elem.tag in tag_mapping:
            readable_title = tag_mapping[elem.tag]
            print(f"{readable_title}: {elem.text}")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
