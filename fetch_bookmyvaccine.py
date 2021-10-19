#!/usr/bin/env python3

import requests
import pandas as pd
import json

all_locations = requests.get("https://maps.bookmyvaccine.covid19.health.nz/booking_site_availability_adhoc.json").json()
permanent  = requests.get("https://maps.bookmyvaccine.covid19.health.nz/booking_site_availability.json").json()

print(f"Found {len(all_locations['features'])} locations, of which {len(permanent['features'])} are permanent")

permanent_ids = [f["properties"]["locationID"] for f in permanent["features"]]
for f in all_locations["features"]:
    p = f["properties"]
    p["adhoc"] = p["locationID"] not in permanent_ids
    p["lng"] = f["geometry"]["coordinates"][0]
    p["lat"] = f["geometry"]["coordinates"][1]

def sort_key(f):
    p = f["properties"]
    return p["dhbRegion"] + str(p["lat"]) + str(p["lng"])
all_locations["features"].sort(key=sort_key)

with open("vaccinations/bookmyvaccine.geojson", "w") as f:
    json.dump(all_locations, f, indent=4)

all_locations = [f["properties"] for f in all_locations["features"]]
pd.DataFrame(all_locations).to_csv("vaccinations/bookmyvaccine.csv", index=False)
