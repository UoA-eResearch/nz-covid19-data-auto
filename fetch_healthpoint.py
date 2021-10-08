#!/usr/bin/env python3

import requests
import os
import json
from pprint import pprint
import pandas as pd
import time

locations = requests.get("https://www.healthpoint.co.nz/geo.do?zoom=18&branch=covid-19-vaccination").json()["results"]
for l in locations:
    l["url"] = "https://www.healthpoint.co.nz" + l["url"]
print(len(locations))
df = pd.DataFrame(locations).sort_values(by=["id", "lat", "lng"])
df.to_csv("vaccinations/healthpoint_locations.csv", index=False)