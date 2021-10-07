#!/usr/bin/env python3

import pandas as pd
import numpy as np
import json

df = pd.read_csv("vaccinations/healthpoint_locations.csv")
df = df.fillna("")
print(df)

features = []
for i, row in df.iterrows():
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row.longitude, row.latitude]
        },
        "properties": row.to_dict()
    })

with open("vaccinations/healthpoint_locations.geojson", "w") as f:
    json.dump({
        "type": "FeatureCollection",
        "features": features
    }, f, indent=4)