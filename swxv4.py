#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import scrolledtext, messagebox, font
import matplotlib.pyplot as plt

# URL of the XML feed
url = "https://www.hamqsl.com/solarxml.php"

# Mapping XML tags to more human-readable titles
tag_mapping = {
    "updated": "Last Updated",
    "solarflux": "Solar Flux",
    "sunspots": "Sunspot Count",
    "aindex": "A-Index",
    "kindex": "K-Index",
    "kindexnt": "K-Index (Non-Telemetered)",
    "xray": "X-Ray Level",
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

solar_data_values = {}
fetched_data_text = ""  # Variable to store fetched data as text

# Fetch solar data function
def fetch_solar_data():
    global fetched_data_text
    try:
        # Fetch the XML data
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the XML data
            root = ET.fromstring(response.content)

            # Display general information about the XML feed
            solar_data = "Solar Activity Information\n" + "=" * 30 + "\n"
            fetched_data_text = ""  # Clear previous data
            global solar_data_values
            solar_data_values = {}

            # Iterate over elements, find human-readable title, and print the values
            for elem in root.iter():
                if elem.tag in tag_mapping:
                    readable_title = tag_mapping[elem.tag]
                    value = elem.text
                    
                    # Check if value is not None
                    if value is not None:
                        try:
                            # Try to store numeric values as float and convert to string for display
                            float_value = float(value)
                            solar_data_values[readable_title] = float_value  # Store as float for plotting
                            value = str(float_value)  # Convert float to string for display
                        except ValueError:
                            pass  # Non-numeric values will be left as is

                    solar_data += f"{readable_title}: {value}\n"
                    fetched_data_text += f"{readable_title}: {value}\n"  # Store for text display

            # Clear the text box and insert the new data
            result_textbox.delete(1.0, tk.END)
            result_textbox.insert(tk.END, solar_data)
            
            # Automatically plot the solar data after fetching it
            plot_solar_data()

        else:
            messagebox.showerror("Error", f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to classify solar data and return color based on propagation conditions
def get_condition_color(label, value):
    if label == "Solar Flux":
        if value < 70:
            return "red", "Propagation potentially bad"
        elif 80 <= value <= 90:
            return "orange", "Propagation somewhat low"
        elif 90 <= value <= 100:
            return "yellow", "Propagation average"
        elif 100 <= value <= 150:
            return "green", "Propagation good"
        else:
            return "blue", "Propagation ideal"
    elif label == "Sunspot Count":
        if value < 50:
            return "red", "Propagation very bad"
        elif 50 <= value <= 75:
            return "orange", "Propagation attenuated"
        elif 75 <= value <= 100:
            return "yellow", "Propagation good"
        elif 100 <= value <= 150:
            return "green", "Propagation ideal"
        else:
            return "blue", "Propagation exceptional"
    elif label == "A-Index":
        if value <= 5:
            return "green", "Best conditions on 10-20 meter bands"
        elif 6 <= value <= 9:
            return "yellow", "Average conditions on 10-20 meter bands"
        else:
            return "red", "Very bad conditions on 10-20 meter bands"
    elif label == "K-Index":
        if value <= 1:
            return "green", "Best conditions on 10-20 meter bands"
        elif 2 <= value <= 3:
            return "yellow", "Good conditions on 10-20 meter bands"
        elif 4 <= value <= 5:
            return "orange", "Average conditions on 10-20 meter bands"
        else:
            return "red", "Very bad conditions on 10-20 meter bands"
    else:
        return "gray", "Unknown condition"

# Function to plot solar data as a bar chart with conditions and show text on the left
def plot_solar_data():
    if not solar_data_values:
        messagebox.showerror("Error", "No data to plot. Please fetch the data first.")
        return

    # Define the order of parameters
    order = ["Sunspot Count", "Solar Flux", "A-Index", "K-Index"]

    labels = []
    values = []
    colors = []
    descriptions = []

    for label in reversed(order):  # Reverse the order of parameters
        if label in solar_data_values:
            value = solar_data_values[label]
            labels.append(label)
            values.append(value)
            color, description = get_condition_color(label, value)
            colors.append(color)
            descriptions.append(f"{label}: {description}")

    if len(values) == 0:
        messagebox.showerror("Error", "No numeric data to plot.")
        return

    plt.figure(figsize=(14, 7))

    # Create subplots: one for the text and one for the bar chart
    ax1 = plt.subplot(1, 2, 1)  # Text display (left)
    ax2 = plt.subplot(1, 2, 2)  # Bar chart display (right)

    # Display the fetched solar data as text in the left subplot, left-justified
    ax1.axis('off')  # Hide axes for the text display
    ax1.text(0, 1, fetched_data_text, fontsize=10, va='top', ha='left', wrap=True)  # Left-justified text
    
    # Plot the solar data as a horizontal bar chart in the right subplot
    bars = ax2.barh(labels, values, color=colors)
    ax2.set_xlabel('Values')
    ax2.set_title('Solar Activity Parameters with Propagation Conditions')

    # Display a summary of the descriptive results to the right of the bar graph
    summary_text = "\n".join(descriptions)
    plt.figtext(0.2, 0.5, summary_text, fontsize=10, ha='left', va='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.show()

# Function to automatically fetch and plot data at regular intervals
def auto_fetch_data():
    fetch_solar_data()  # Fetch and plot the data
    root.after(7200000, auto_fetch_data)  # Re-fetch every 2 hours (7200000 ms)

# Create the main window
root = tk.Tk()
root.title("Solar Activity Information")
root.geometry("500x500")

# Create a text box with a scrollbar for displaying the results
result_textbox = scrolledtext.ScrolledText(root, width=60, height=20)
result_textbox.pack(pady=10)

# Create a larger font for the buttons
button_font = font.Font(size=12, weight='bold')

# Create a button to fetch the solar data (for manual use)
fetch_button = tk.Button(root, text="Fetch Solar Data", command=fetch_solar_data, width=20, height=2, font=button_font)
fetch_button.pack(pady=10)

# Fetch data once on startup, then every 2 hours
auto_fetch_data()

# Run the main event loop
root.mainloop()

