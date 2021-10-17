#!/usr/bin/env python3

import requests
import pandas as pd
import numpy as np

FILENAME = "vaccinations/healthpoint_locations.csv"
existing = pd.read_csv(FILENAME)

locations = requests.get("https://www.healthpoint.co.nz/geo.do?zoom=18&branch=covid-19-vaccination").json()["results"]
for i, l in enumerate(locations):
    l["url"] = "https://www.healthpoint.co.nz" + l["url"]
    existing_location_different_id = existing[
        np.isclose(existing.lat, l["lat"]) &
        np.isclose(existing.lng, l["lng"]) &
        (existing.name == l["name"]) &
        (existing.url == l["url"]) &
        (existing.id != l["id"])
    ]
    if len(existing_location_different_id):
        print(f"Ignoring minor change:\n{existing_location_different_id.to_dict(orient='records')[0]} ->\n{l}")
        l["id"] = existing_location_different_id.id.iloc[0]
        l["branch"] = existing_location_different_id.branch.iloc[0]
print(len(locations))
df = pd.DataFrame(locations).sort_values(by=["id", "lat", "lng"])
df.to_csv("vaccinations/healthpoint_locations.csv", index=False)
