#!/usr/bin/env python3

import requests
import re
import os
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO

url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-data-and-statistics/covid-19-case-demographics"
url += f"?{time.time()}"
r = requests.get(url)
soup = BeautifulSoup(r.content)
link = soup.find("a", href=re.compile("csv"))
link = "https://www.health.govt.nz" + link["href"]
print(link)

force = False

if not force and os.path.isfile("last_link.txt"):
    with open("last_link.txt", "r") as f:
        last_link = f.read()
        if link == last_link:
            print("already done, exiting")
            exit(1)
with open("last_link.txt", "w") as f:
    f.write(link)

r = requests.get(link)
data = StringIO(r.text)
headers = ["Report Date", "Case Status", "Sex", "Age group", "DHB", "Overseas travel"]
df = pd.read_csv(data, header=0, names=headers, skip_blank_lines=True)
df = df.sort_values(by=headers, ascending=False)
df.to_csv("data.csv", index=False)
print(df)
