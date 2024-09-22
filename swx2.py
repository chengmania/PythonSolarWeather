#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET

# URL of the XML feed
url = "https://www.hamqsl.com/solarxml.php"

# ANSI escape codes for text formatting
BOLD = '\033[1m'
RESET = '\033[0m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BLUE = '\033[34m'
CYAN = '\033[36m'

# Mapping XML tags to more human-readable titles
tag_mapping = {
    "updated": "Last Updated",
    "solarflux": "Solar Flux",
    "sunspots": "Sunspot Count",
    "aindex": "A-Index",
    "kindex": "K-Index",
    "xray": "X-Ray Level",
    "heliumline": "Helium Line",
    "protonflux": "Proton Flux",
    "aurora": "Aurora Level",
    "normalization": "Normalization Factor",
    "solarwind": "Solar Wind Speed",
    "magneticfield": "Magnetic Field Strength",
    "geomagfield": "Geomagnetic Field",
    "signalnoise": "Signal Noise Level",
    "fof2": "Critical Frequency foF2",
    "muf": "Maximum Usable Frequency"
}

# Initialize dictionary to hold all possible values
data = {key: None for key in tag_mapping}

# Fetch the XML data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML data
    root = ET.fromstring(response.content)

    # Populate data dictionary with values from XML
    for elem in root.iter():
        if elem.tag in data:
            data[elem.tag] = elem.text

    # Display all fetched information with proper formatting
    print(f"{BOLD}{CYAN}Solar Activity Information{RESET}\n" + "="*40)

    label_width = 25  # Set a fixed width for the label
    value_width = 10  # Set a fixed width for the value

    for tag, readable_title in tag_mapping.items():
        value = data[tag] if data[tag] is not None else "No data"
        print(f"{BOLD}{readable_title:<{label_width}}{RESET}: {value:>{value_width}}")

    # Extract specific values for propagation summary
    solar_flux = float(data["solarflux"]) if data["solarflux"] else None
    sunspots = int(data["sunspots"]) if data["sunspots"] else None
    a_index = int(data["aindex"]) if data["aindex"] else None
    k_index = int(data["kindex"]) if data["kindex"] else None
    signal_noise = data["signalnoise"].strip() if data["signalnoise"] else None  # Stripping extra whitespace

    # Provide summary for propagation conditions
    print(f"\n{BOLD}{BLUE}Propagation Summary{RESET}\n" + "="*50)

    # Summary for Solar Flux Index (SFI)
    if solar_flux is not None:
        print(f"{BOLD}Solar Flux Index (SFI):{RESET} {solar_flux}")
        if solar_flux < 70:
            print(f"{RED}... Propagation potentially bad due to low solar flux.{RESET}")
        elif 80 <= solar_flux < 90:
            print(f"{YELLOW}... Propagation is somewhat low but still usable.{RESET}")
        elif 90 <= solar_flux < 100:
            print(f"{GREEN}... Propagation is average, conditions are acceptable.{RESET}")
        elif 100 <= solar_flux < 150:
            print(f"{GREEN}... Propagation is good; conditions are favorable.{RESET}")
        elif solar_flux > 150:
            print(f"{GREEN}... Propagation is ideal, expect excellent conditions.{RESET}")

    # Summary for Sunspot Numbers (SN)
    if sunspots is not None:
        print(f"")
        print(f"{BOLD}Sunspot Numbers:{RESET} {sunspots}")
        if sunspots < 50:
            print(f"{RED}... Propagation conditions potentially very bad due to low sunspot numbers.{RESET}")
        elif 50 <= sunspots < 75:
            print(f"{YELLOW}... Propagation is attenuated, but not the worst.{RESET}")
        elif 75 <= sunspots < 100:
            print(f"{GREEN}... Propagation conditions are good.{RESET}")
        elif 100 <= sunspots < 150:
            print(f"{GREEN}... Propagation conditions are ideal.{RESET}")
        elif sunspots > 150:
            print(f"{GREEN}... Propagation conditions could be exceptional.{RESET}")

    # Summary for A-Index
    if a_index is not None:
        print(f"")
        print(f"{BOLD}A-Index:{RESET} {a_index}")
        if 1 <= a_index <= 5:
            print(f"{GREEN}... Best conditions on 10-20 meter bands.{RESET}")
        elif 6 <= a_index <= 9:
            print(f"{YELLOW}... Average conditions on 10-20 meter bands.{RESET}")
        elif a_index > 10:
            print(f"{RED}... Very bad conditions on 10-20 meter bands.{RESET}")

    # Summary for K-Index
    if k_index is not None:
        print(f"")
        print(f"{BOLD}K-Index:{RESET} {k_index}")
        if 0 <= k_index <= 1:
            print(f"{GREEN}... Best conditions for 10-20 meter bands.{RESET}")
        elif 2 <= k_index <= 3:
            print(f"{YELLOW}... Good conditions for 10-20 meter bands.{RESET}")
        elif 4 <= k_index <= 5:
            print(f"{YELLOW}... Average conditions for 10-20 meter bands.{RESET}")
        elif k_index > 5:
            print(f"{RED}...Very bad conditions for 10-20 meter bands.{RESET}")

    # Condensed Summary for Signal to Noise Level
    if signal_noise is not None:
        print(f"")
        print(f"{BOLD}Background Signal to Noise Level:{RESET} {signal_noise}")
        print(f"{GREEN}... S0-S2: Low Noise or Quiet environment.{RESET}")
        print(f"{YELLOW}... S3-S5: Moderate Noise or Some interference.{RESET}")
        print(f"{RED}... S6-S9: High Noise or High interference.{RESET}")

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    
print(f"")
print(f"")

