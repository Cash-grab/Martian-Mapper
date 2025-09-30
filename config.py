import os
import requests
import json
NASA_API_KEY = os.environ.get('NASA_API_KEY', 'FWfMV1Y4DLpABZHUGbW9MhMMej3yA12XucJ4YR1a')

file_name = "static/json/roverdata.json"

if os.path.exists(file_name):
        print(f"Found Cached data '{file_name}'.")
        
        # Perform actions if the file exists
else:

    print(f"The file '{file_name}' does not exist. Fetching new data from NASA API...")
    roverurl = f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={NASA_API_KEY}"
    roverresp = requests.get(roverurl)
    roverdata = roverresp.json()
    with open(file_name, 'w') as f:
        json.dump(roverdata, f, indent=4)
# Perform actions if the file does not exist