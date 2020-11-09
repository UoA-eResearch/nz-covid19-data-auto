#!/usr/bin/env python3

import requests
import pandas as pd
from io import StringIO

session = "93847a240fe248bf634f298ec2410d2f"
cookie = "route=1604958355.109.13309.111578"

r = requests.get(f"https://nzcoviddashboard.esr.cri.nz/session/{session}/download/overview-downloadCurveData", headers={
    "Cookie": cookie
})

data = StringIO(r.text)
df = pd.read_csv(data, skiprows=3, skip_blank_lines=True)
df = df.dropna()
print(df)

df.to_csv("cases_by_DHB_over_time.csv")