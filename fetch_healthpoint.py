#!/usr/bin/env python3

import requests
import os
import json
from pprint import pprint
import pandas as pd
import time

DEBUG = False

if DEBUG and os.path.isfile("healthpoint.json"):
    with open("healthpoint.json") as f:
        entries = json.load(f)
else:
    entries = []
    API_KEY = os.environ["APIKEY"]
    url = "https://uat.healthpointapi.com/baseR4/HealthcareService?services-provided-type=COVID-19%20Vaccination&_count=200" # Max 200 entries
    while url:
        print(f"Fetching {url}")
        resp = requests.get(url, headers={"x-api-key": API_KEY}).json()
        print(f"Got {len(resp['entry'])} entries")
        entries.extend(resp["entry"])
        url = None
        pprint(resp["link"])
        for link in resp["link"]:
            if link["relation"] == "next":
                url = link["url"]
        time.sleep(1)
    with open("healthpoint.json", "w") as f:
        json.dump(entries, f)

locations = []
if len(entries) < 200:
    print(f"Only got {len(entries)} entries, something's wrong, aborting")
    exit(1)

for entry in entries:
    for e in entry["resource"].get("extension"):
        eeInfo = {}
        if entry["resource"].get("name"):
            eeInfo["name"] = entry["resource"].get("name")
        location = {}
        for ee in e.get("extension", []):
            if "valueString" in ee:
                eeInfo[ee["url"]] = ee["valueString"]
            if ee["url"] == "services-provided":
                serviceDict = {}
                for eee in ee["extension"]:
                    k = eee["url"]
                    v = eee.get("valueString")
                    if k in serviceDict:
                        if type(serviceDict[k]) == str:
                            serviceDict[k] = [serviceDict[k], v]
                        else:
                            serviceDict[k].append(v)
                    else:
                        serviceDict[k] = v
                if serviceDict["services-name"] == "COVID-19 Vaccination":
                    eeInfo.update(serviceDict)
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