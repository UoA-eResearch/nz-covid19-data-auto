#!/usr/bin/env python3

import requests
import os
import json
from pprint import pprint
import pandas as pd
import time

entries = []
API_KEY = os.environ["APIKEY"]
url = "https://uat.healthpointapi.com/baseR4/HealthcareService?services-provided-type=COVID-19%20Vaccination&_count=200" # Max 200 entries
while url:
    print(f"Fetching {url}")
    resp = requests.get(url, headers={"x-api-key": API_KEY}).json()
    print(f"Got {len(resp['entry'])} entries")
    entries.extend(resp["entry"])
    url = None
    for link in resp["link"]:
        if link["relation"] == "next":
            url = link["url"]
    time.sleep(1)

locations = []

for entry in entries:
    for e in entry["resource"].get("extension"):
        eeInfo = {}
        for ee in e.get("extension", []):
            if "valueString" in ee:
                eeInfo[ee["url"]] = ee["valueString"]
            if ee["url"] == "service-location":
                location = eeInfo.copy()
                for eee in ee["extension"]:
                    if eee["url"] == "location":
                        location[eee["url"]] = eee["valueReference"]["display"]
                    elif eee["url"] == "coordinates":
                        for eeee in eee["extension"]:
                            location[eeee["url"]] = eeee["valueDecimal"]
                    elif eee["url"] in ["hours-description", "hp-location-url"]:
                        location["url"] = eee["valueString"]
        if location.get("location"):
            locations.append(location)

#pprint(locations)
print(len(locations))
df = pd.DataFrame(locations)
df.to_csv("vaccinations/healthpoint_locations.csv", index=False)