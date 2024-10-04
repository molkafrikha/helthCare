import requests
from bs4 import BeautifulSoup
import json
import time

# Step 1: Access the main page and get all device links
url = "https://www.devicespecifications.com/en/brand/1e7667"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Step 2: Find all device links
device_links = [a['href'] for a in soup.select("div.model-listing-container-80 a")]

# Debugging: print the number of device links found
print(f"Found {len(device_links)} device links")

# Step 3: Extract camera specifications for each device
camera_specs = []

for link in device_links:

    try:
        device_response = requests.get(link)
        device_soup = BeautifulSoup(device_response.content, "html.parser")

        # Extract device name from the title tag
        device_name = device_soup.title.string.split(" - ")[0]

        # Initialize dictionary to store camera specs
        device_camera_specs = {"device_name": device_name, "rear_camera": {}, "front_camera": {}}

        # Find the 'Rear camera' specs
        rear_camera_section = device_soup.find("h2", string="Rear camera")
        if rear_camera_section:
            rear_camera_table = rear_camera_section.find_next("table", class_="model-information-table")
            if rear_camera_table:
                for row in rear_camera_table.find_all("tr"):
                    key = row.find("td").text.split("Information")[0].strip()
                    value = row.find_all("td")[1].text.strip()
                    if "Image resolution" in key:
                        device_camera_specs["rear_camera"]["Image resolution"] = value.split()[0] + " MP"

        # Find the 'Front camera' specs
        front_camera_section = device_soup.find("h2", string="Front camera")
        if front_camera_section:
            front_camera_table = front_camera_section.find_next("table", class_="model-information-table")
            if front_camera_table:
                for row in front_camera_table.find_all("tr"):
                    key = row.find("td").text.split("Information")[0].strip()
                    value = row.find_all("td")[1].text.strip()
                    if "Image resolution" in key:
                        device_camera_specs["front_camera"]["Image resolution"] = value.split()[0] + " MP"

        camera_specs.append(device_camera_specs)

        # Debugging: print the device name and camera specs for each device
        print(json.dumps(device_camera_specs, indent=4))

        # Pause briefly to avoid overwhelming the server
        time.sleep(1)

    except Exception as e:
        print(f"Failed to retrieve data for {link}: {e}")

# Step 4: Convert the data into JSON format
camera_specs_json = json.dumps(camera_specs, indent=4)

# Save the JSON data to a file
with open("data/camera_specs1-293.json", "w") as file:
    file.write(camera_specs_json)

print("Camera specifications have been saved to camera_specs1-293.json")
